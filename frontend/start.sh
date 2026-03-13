#!/bin/bash
# 启动前端开发服务器

cd "$(dirname "$0")"

# 检查是否安装了依赖
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "启动 Vue.js 开发服务器..."
npm run dev