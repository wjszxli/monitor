#!/bin/bash
# Cron 环境下的调试：将所有输出重定向到日志文件
exec >> /Users/huasheng/learn/monitor/monitor.log 2>> /Users/huasheng/learn/monitor/monitor.err

echo "---"
echo "Cron job started at: $(date)"

echo "Changing directory to /Users/huasheng/learn/monitor"
cd /Users/huasheng/learn/monitor
echo "Current directory: $(pwd)"

echo "Executing python script with /Users/huasheng/.pyenv/versions/3.10.5/bin/python3"
/Users/huasheng/.pyenv/versions/3.10.5/bin/python3 /Users/huasheng/learn/monitor/monitor.py
echo "Python script finished."