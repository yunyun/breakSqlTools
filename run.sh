#!/bin/bash

ROOT=$(cd `dirname $0`; pwd)"/"
cd $ROOT

VENV_DIR="venv"

# 检查虚拟环境是否存在
if [ -d "$VENV_DIR/bin" ]; then
    echo "虚拟环境已存在，正在激活..."
    source "$VENV_DIR/bin/activate"
else
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
fi

# 运行Python脚本
echo "正在运行数据库备份Python脚本 main.py"
python main.py

# 脚本结束后，虚拟环境将自动“失效”，因为激活是通过修改当前shell的环境变量实现的
# 如果您希望提示用户如何关闭虚拟环境，可以在这里添加一条消息
# echo "虚拟环境已自动‘失效’。如果您在脚本执行前手动激活了虚拟环境，请记得使用‘deactivate’命令关闭它。"