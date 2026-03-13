#!/bin/bash
# 生产环境部署脚本

set -e

echo "🚀 开始部署儿童故事生成器到生产环境..."

# 1. 后端部署
echo "🔧 部署后端服务..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装 Python 依赖..."
pip install -r requirements.txt

# 创建 systemd 服务文件
sudo tee /etc/systemd/system/kids-story-backend.service > /dev/null << EOF
[Unit]
Description=Kids Story Generator Backend
After=network.target

[Service]
Type=exec
User=admin
WorkingDirectory=/home/admin/openclaw/workspace/kids-story-generator/backend
Environment=PATH=/home/admin/openclaw/workspace/kids-story-generator/backend/venv/bin
ExecStart=/home/admin/openclaw/workspace/kids-story-generator/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动后端服务
sudo systemctl daemon-reload
sudo systemctl enable kids-story-backend
sudo systemctl restart kids-story-backend

echo "✅ 后端服务已启动 (端口 8000)"

# 2. 前端构建
echo "🏗️ 构建前端应用..."
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 3. 配置 Nginx (如果已安装)
if command -v nginx &> /dev/null; then
    echo "⚙️ 配置 Nginx 反向代理..."
    
    sudo tee /etc/nginx/sites-available/kids-story-generator > /dev/null << EOF
server {
    listen 80;
    server_name _;  # 替换为你的域名或 IP
    
    # 前端静态文件
    location / {
        root /home/admin/openclaw/workspace/kids-story-generator/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        index index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    
    # 启用站点
    sudo ln -sf /etc/nginx/sites-available/kids-story-generator /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
    
    echo "✅ Nginx 配置完成"
    echo "🌐 应用可通过 http://你的服务器IP 访问"
else
    echo "⚠️ Nginx 未安装，你可以："
    echo "   1. 手动安装 Nginx: sudo apt install nginx"
    echo "   2. 或者直接访问前端开发服务器 (需要额外配置)"
    echo "   3. 或者使用其他 Web 服务器"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "后端 API: http://你的服务器IP:8000"
echo "前端应用: http://你的服务器IP"
echo ""
echo "💡 注意：请将 '你的服务器IP' 替换为实际的公网 IP 地址"
echo "💡 如果有域名，请在 Nginx 配置中替换 server_name"

# 显示服务状态
echo ""
echo "📊 服务状态:"
sudo systemctl status kids-story-backend --no-pager