#!/bin/bash

# 获取脚本所在的绝对路径
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Cron 环境下的调试：将所有输出重定向到日志文件
# 日志文件将与脚本在同一目录下
exec >> "${SCRIPT_DIR}/monitor.log" 2>> "${SCRIPT_DIR}/monitor.err"

echo "---"
echo "Cron job started at: $(date)"

# 切换到脚本所在目录, 确保所有相对路径都正确
cd "${SCRIPT_DIR}"
echo "Current directory: $(pwd)"

echo "Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt

echo "Executing python script..."
# 使用 'python3' 命令, 假设它在用户的 PATH 中
# 或者, 如果 monitor.py 有可执行权限并且 shebang 正确, 可以直接运行 ./monitor.py
python3 monitor.py
echo "Python script finished."
