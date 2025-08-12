#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import json
import time
from urllib.parse import urljoin

# --- 全局变量 ---
# 脚本所在的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 配置文件路径
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
# 历史记录文件路径
ANNOUNCEMENTS_FILE = os.path.join(SCRIPT_DIR, "announcements.json")
# 全局配置
CONFIG = {}


def load_config():
    """
    从 config.json 加载配置。
    """
    global CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {CONFIG_FILE}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {CONFIG_FILE}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}")
        exit(1)


def send_notification(title, body):
    """
    使用 ServerChan 发送通知。
    """
    send_key = CONFIG.get("server_chan_send_key")
    if not send_key or send_key == "YOUR_SERVERCHAN_SENDKEY":
        print("Notification service is not configured. Skipping.")
        return

    api_url = f"https://sctapi.ftqq.com/{send_key}.send"
    payload = {"title": title, "desp": body}
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()
        result = response.json()
        if result.get("code") == 0:
            print(f"Notification sent successfully for: {title}")
        else:
            print(f"Failed to send notification. Reason: {result.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during notification sending: {e}")


def get_latest_announcements(site_config):
    """
    获取单个网站最新的N条公告。
    返回一个包含 {title, url} 字典的列表。
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36)"
        }
        response = requests.get(site_config["url"], headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        container = soup.select_one(site_config["selectors"]["list_container"])
        if not container:
            print(
                f"Error for '{site_config['name']}': Could not find list container with selector '{site_config['selectors']['list_container']}'."
            )
            return []

        items = container.select(site_config["selectors"]["list_item"])
        if CONFIG.get("monitor_count", 0) > 0:
            items = items[: CONFIG["monitor_count"]]

        announcements = []
        for item in items:
            link = item.select_one(site_config["selectors"]["link"])
            if link and link.get("title") and link.get("href"):
                full_url = urljoin(
                    site_config.get("base_url", site_config["url"]), link.get("href")
                )
                announcements.append(
                    {"title": link.get("title").strip(), "url": full_url}
                )
        return announcements
    except requests.exceptions.RequestException as e:
        print(f"Error fetching '{site_config['name']}': {e}")
        return []
    except Exception as e:
        print(f"An error occurred while parsing '{site_config['name']}': {e}")
        return []


def load_history():
    """
    从JSON文件加载所有站点的历史公告。
    """
    if not os.path.exists(ANNOUNCEMENTS_FILE):
        return {}
    try:
        with open(ANNOUNCEMENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, TypeError):
        print(
            f"Warning: Could not decode JSON from {ANNOUNCEMENTS_FILE}. Starting fresh."
        )
        return {}
    except Exception as e:
        print(f"Error loading history from {ANNOUNCEMENTS_FILE}: {e}")
        return {}


def save_history(history_data):
    """
    将所有站点的历史公告保存到JSON文件。
    """
    try:
        with open(ANNOUNCEMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving history to {ANNOUNCEMENTS_FILE}: {e}")


def check_site(site_config, history):
    """
    检查单个站点，并在有更新时发送通知。
    """
    site_name = site_config["name"]
    print(f"\n--- Checking site: {site_name} ---")

    # 1. 获取最新公告
    latest_announcements = get_latest_announcements(site_config)
    if not latest_announcements:
        print("Could not retrieve any announcements. Skipping.")
        print(f"--- Finished checking {site_name} ---")
        return

    latest_urls = {ann["url"] for ann in latest_announcements}

    # 2. 加载特定站点的历史
    old_urls = set(history.get(site_name, []))

    # 3. 找出新公告
    new_urls = latest_urls - old_urls

    if new_urls:
        print(f"Found {len(new_urls)} new announcement(s) for {site_name}!")
        new_items = [ann for ann in latest_announcements if ann["url"] in new_urls]

        # 汇总所有新公告为一条消息
        title = f"【{site_name}】发现 {len(new_urls)} 条新公告"

        body_parts = []
        # 网站上新消息在最前，我们正序处理，让最新的消息在通知的顶部
        for item in new_items:
            print(f"  - Title: {item['title']}")
            print(f"    URL: {item['url']}")
            body_parts.append(f"标题：{item['title']}\n链接：{item['url']}")

        body = "\n\n---\n\n".join(body_parts)
        send_notification(title, body)

        # 4. 更新该站点的历史记录
        print(f"Updating history for {site_name}...")
        history[site_name] = list(latest_urls)
    else:
        print("No new announcements since the last check.")
    
    print(f"--- Finished checking {site_name} ---")


def main():
    """
    主函数，执行所有已启用站点的监控。
    """
    print(f"--- Starting check cycle at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")

    load_config()

    all_history = load_history()
    original_history = all_history.copy()

    for site_config in CONFIG.get("sites", []):
        if site_config.get("enabled", False):
            check_site(site_config, all_history)
        else:
            print(f"\n--- Skipping disabled site: {site_config['name']} ---")

    # 如果历史记录有变动，则保存
    if all_history != original_history:
        save_history(all_history)

    print("\n--- Check cycle finished ---")


if __name__ == "__main__":
    main()
