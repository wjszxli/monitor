# Website Announcement Monitor | 网站公告监控器

[English](#website-announcement-monitor) | [中文](#网站公告监控器)

---

## Website Announcement Monitor

A flexible and powerful monitoring tool that keeps an eye on important announcements on any website for you. Never miss an update again!

Whether it's exam schedules, policy changes, or the latest news from your favorite institution, this monitor will notify you instantly as soon as new information is published.

### ✨ Features

- **Monitor Any Website**: Easily configure it to watch any number of websites.
- **Precise Targeting**: Uses CSS selectors to pinpoint the exact announcement list on a page.
- **Instant Notifications**: Get real-time alerts via [ServerChan](https://sct.ftqq.com/) when new announcements are found.
- **Easy to Set Up**: Get started in minutes with a simple JSON configuration.
- **Lightweight & Reliable**: Runs efficiently in the background with a single Python script.

### 🚀 Getting Started

#### Prerequisites

- Python 3
- `pip` (Python package installer)

#### Installation & Configuration

1.  **Clone or download this repository.**

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *The `requirements.txt` file should contain:*
    ```
    requests
    beautifulsoup4
    lxml
    ```

3.  **Configure the monitor:**
    - Rename `config.example.json` to `config.json`. (You will need to create this file based on the example below).
    - Open `config.json` and edit it following the instructions in the **Configuration** section.

### ⚙️ Configuration

The `config.json` file is the heart of the monitor. Here’s how to set it up:

```json
{
  "server_chan_send_key": "YOUR_SERVERCHAN_SENDKEY",
  "monitor_count": 5,
  "sites": [
    {
      "name": "Example University News",
      "url": "https://www.example.edu/news",
      "enabled": true,
      "base_url": "https://www.example.edu",
      "selectors": {
        "list_container": "div.news-list ul",
        "list_item": "li",
        "link": "a"
      }
    },
    {
      "name": "Another Website Announcements",
      "url": "https://www.another-site.com/announcements",
      "enabled": true,
      "base_url": "https://www.another-site.com",
      "selectors": {
        "list_container": ".post-container",
        "list_item": ".post-item",
        "link": "a.post-title-link"
      }
    },
    {
      "name": "Disabled Example",
      "url": "https://www.disabled.com",
      "enabled": false,
      "selectors": {}
    }
  ]
}
```

**Field Explanation:**

- `server_chan_send_key`: **(Required)** Your personal key from ServerChan for receiving notifications. Get one [here](https://sct.ftqq.com/).
- `monitor_count`: **(Optional)** The number of latest announcements to check on each site. If set to `0` or omitted, it checks all items found in the container.
- `sites`: A list of websites to monitor.
    - `name`: A custom name for the website (e.g., "University Admissions").
    - `url`: The URL of the page with the announcement list.
    - `enabled`: Set to `true` to monitor this site, `false` to disable it.
    - `base_url`: **(Optional)** The base URL used to construct absolute links if the links in the page are relative (e.g., `/news/123`). Defaults to the `url` if not provided.
    - `selectors`: CSS selectors to find the announcements.
        - `list_container`: Selector for the element that contains the list of announcements (e.g., `div.news-list ul`).
        - `list_item`: Selector for a single announcement item within the container (e.g., `li`).
        - `link`: Selector for the link (`<a>` tag) inside the list item. The monitor extracts the link's `href` and `title` attributes.

### ▶️ Usage

#### Manual Execution

You can run the monitor manually at any time:

```bash
python3 monitor.py
```

#### Automated Execution with Cron

For continuous monitoring, you can set up a cron job. The included `start_monitor.sh` script is perfect for this.

1.  **Make the script executable:**
    ```bash
    chmod +x start_monitor.sh
    ```

2.  **Edit your crontab:**
    ```bash
    crontab -e
    ```

3.  **Add a new line to run the script at your desired interval.** For example, to run it every 30 minutes:
    ```cron
    */30 * * * * /path/to/your/project/start_monitor.sh
    ```
    *Make sure to replace `/path/to/your/project/` with the absolute path to the project directory.*

---
---

## 网站公告监控器

一个灵活又强大的监控工具，为你时刻关注任何网站上的重要公告。从此不再错过任何更新！

无论是考试安排、政策变动，还是你关心的机构发布的最新通知，这个监控器都能在信息发布的第一时间即时通知你。

### ✨ 功能特性

- **监控任意网站**：只需简单配置，即可监控任意数量的网站。
- **精确定位**：使用 CSS 选择器，精确锁定页面上的公告列表。
- **即时通知**：发现新公告时，通过 [ServerChan](https://sct.ftqq.com/) 获取实时推送提醒。
- **设置简单**：仅需一个简单的 JSON 配置文件，几分钟内即可开始使用。
- **轻量可靠**：单个 Python 脚本，可在后台高效运行。

### 🚀 快速上手

#### 环境要求

- Python 3
- `pip` (Python 包管理工具)

#### 安装与配置

1.  **克隆或下载本项目代码。**

2.  **安装依赖包：**
    ```bash
    pip install -r requirements.txt
    ```
    *`requirements.txt` 文件应包含以下内容:*
    ```
    requests
    beautifulsoup4
    lxml
    ```

3.  **配置监控器：**
    - 将 `config.example.json` 重命名为 `config.json`。（你需要根据下面的示例创建一个 `config.json` 文件）。
    - 打开 `config.json` 文件，参考下方的**配置说明**进行编辑。

### ⚙️ 配置说明

`config.json` 文件是监控器的核心。以下是配置方法：

```json
{
  "server_chan_send_key": "你的_SERVERCHAN_SENDKEY",
  "monitor_count": 5,
  "sites": [
    {
      "name": "示例大学新闻",
      "url": "https://www.example.edu/news",
      "enabled": true,
      "base_url": "https://www.example.edu",
      "selectors": {
        "list_container": "div.news-list ul",
        "list_item": "li",
        "link": "a"
      }
    },
    {
      "name": "另一个网站的公告",
      "url": "https://www.another-site.com/announcements",
      "enabled": true,
      "base_url": "https://www.another-site.com",
      "selectors": {
        "list_container": ".post-container",
        "list_item": ".post-item",
        "link": "a.post-title-link"
      }
    },
    {
      "name": "已禁用的示例",
      "url": "https://www.disabled.com",
      "enabled": false,
      "selectors": {}
    }
  ]
}
```

**字段解释:**

- `server_chan_send_key`: **(必需)** 你在 ServerChan 获取的个人推送 KEY。可以从 [这里](https://sct.ftqq.com/) 获取。
- `monitor_count`: **(可选)** 每次检查时，获取每个网站最新的几条公告。如果设为 `0` 或省略，则检查容器内所有项目。
- `sites`: 需要监控的网站列表。
    - `name`: 自定义网站名称（例如：“大学招生网”）。
    - `url`: 公告列表所在页面的 URL。
    - `enabled`: `true` 表示监控该网站，`false` 表示禁用。
    - `base_url`: **(可选)** 用于拼接相对链接的根 URL（例如，页面上的链接是 `/news/123`）。如果未提供，则默认使用 `url` 的值。
    - `selectors`: 用于查找公告的 CSS 选择器。
        - `list_container`: 包含公告列表的元素的 CSS 选择器（例如 `div.news-list ul`）。
        - `list_item`: 列表容器中单个公告条目的选择器（例�� `li`）。
        - `link`: 公告条目中链接（`<a>` 标签）的选择器。监控器会提取其 `href` 和 `title` 属性。

### ▶️ 如何使用

#### 手动执行

你可以随时手动运行监控脚本：

```bash
python3 monitor.py
```

#### 使用 Cron 自动执行

为了实现持续监控，你可以设置一个定时任务（Cron Job）。项目附带的 `start_monitor.sh` 脚本非常适合此场景。

1.  **为脚本添加可执行权限：**
    ```bash
    chmod +x start_monitor.sh
    ```

2.  **编辑你的 crontab：**
    ```bash
    crontab -e
    ```

3.  **添加新的一行，设置你希望的执行周期。** 例如，每 30 分钟执行一次：
    ```cron
    */30 * * * * /path/to/your/project/start_monitor.sh
    ```
    *请务必将 `/path/to/your/project/` 替换为项目所在的绝对路径。*
