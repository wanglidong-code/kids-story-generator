#!/bin/bash
# 启动后端服务

cd "$(dirname "$0")"

# 检查是否安装了依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "requirements.installed" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
    touch requirements.installed
fi

echo "启动 FastAPI 服务..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload