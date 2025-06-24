#!/bin/bash

# joj达电梯科技 - 自动部署脚本
# 部署到 ailingjing.cn

set -e  # 遇到错误时退出

echo "🚀 开始部署 joj达电梯科技到 ailingjing.cn..."

# 配置变量
DOMAIN="ailingjing.cn"
SERVER_USER="your_username"
SERVER_IP="your_server_ip"
LOCAL_BUILD_DIR="build"
REMOTE_WEB_DIR="/var/www/${DOMAIN}/html"
NGINX_CONFIG="/etc/nginx/sites-available/${DOMAIN}"
BACKUP_DIR="/var/backups/website-$(date +%Y%m%d-%H%M%S)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 检查本地构建文件
if [ ! -d "$LOCAL_BUILD_DIR" ]; then
    print_error "构建目录 $LOCAL_BUILD_DIR 不存在！"
    echo "请先运行: npm run build"
    exit 1
fi

print_status "本地构建文件检查完成"

# 检查服务器连接
if ! ssh -q -o ConnectTimeout=5 "$SERVER_USER@$SERVER_IP" exit; then
    print_error "无法连接到服务器 $SERVER_IP"
    echo "请检查："
    echo "1. 服务器IP地址是否正确"
    echo "2. SSH密钥是否配置正确"
    echo "3. 服务器是否在线"
    exit 1
fi

print_status "服务器连接检查完成"

# 备份现有网站（如果存在）
echo "📦 备份现有网站..."
ssh "$SERVER_USER@$SERVER_IP" "
    if [ -d '$REMOTE_WEB_DIR' ]; then
        sudo mkdir -p '$BACKUP_DIR'
        sudo cp -r '$REMOTE_WEB_DIR'/* '$BACKUP_DIR'/ 2>/dev/null || true
        echo '备份创建于: $BACKUP_DIR'
    fi
"

print_status "网站备份完成"

# 创建必要的目录
echo "📁 创建部署目录..."
ssh "$SERVER_USER@$SERVER_IP" "
    sudo mkdir -p '$REMOTE_WEB_DIR'
    sudo chown -R \$USER:www-data '$REMOTE_WEB_DIR'
    sudo chmod -R 755 '$REMOTE_WEB_DIR'
"

print_status "目录创建完成"

# 上传文件
echo "📤 上传网站文件..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='*.log' \
    "$LOCAL_BUILD_DIR/" "$SERVER_USER@$SERVER_IP:$REMOTE_WEB_DIR/"

print_status "文件上传完成"

# 设置正确的权限
echo "🔐 设置文件权限..."
ssh "$SERVER_USER@$SERVER_IP" "
    sudo chown -R www-data:www-data '$REMOTE_WEB_DIR'
    sudo find '$REMOTE_WEB_DIR' -type d -exec chmod 755 {} \;
    sudo find '$REMOTE_WEB_DIR' -type f -exec chmod 644 {} \;
"

print_status "文件权限设置完成"

# 上传并配置 Nginx
echo "⚙️ 配置 Nginx..."
scp "deployment/nginx.conf" "$SERVER_USER@$SERVER_IP:/tmp/nginx-${DOMAIN}.conf"

ssh "$SERVER_USER@$SERVER_IP" "
    # 备份现有配置
    if [ -f '$NGINX_CONFIG' ]; then
        sudo cp '$NGINX_CONFIG' '$NGINX_CONFIG.backup-\$(date +%Y%m%d-%H%M%S)'
    fi
    
    # 安装新配置
    sudo mv '/tmp/nginx-${DOMAIN}.conf' '$NGINX_CONFIG'
    
    # 启用站点
    sudo ln -sf '$NGINX_CONFIG' '/etc/nginx/sites-enabled/${DOMAIN}'
    
    # 测试配置
    sudo nginx -t
    
    # 重新加载 Nginx
    sudo systemctl reload nginx
"

print_status "Nginx 配置完成"

# 部署后端API（如果需要）
echo "🔧 部署后端服务..."
if [ -d "server-dotnet" ]; then
    # 打包后端
    tar -czf backend-$(date +%Y%m%d-%H%M%S).tar.gz server-dotnet/
    
    # 上传后端文件
    scp "backend-*.tar.gz" "$SERVER_USER@$SERVER_IP:/tmp/"
    
    ssh "$SERVER_USER@$SERVER_IP" "
        # 创建后端目录
        sudo mkdir -p '/var/www/${DOMAIN}/api'
        
        # 解压后端文件
        cd '/var/www/${DOMAIN}/api'
        sudo tar -xzf '/tmp/backend-*.tar.gz' --strip-components=1
        
        # 安装.NET运行时（如果未安装）
        if ! command -v dotnet &> /dev/null; then
            wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
            chmod +x dotnet-install.sh
            ./dotnet-install.sh --channel 8.0
            export PATH=\$PATH:\$HOME/.dotnet
        fi
        
        # 构建和运行后端
        cd '/var/www/${DOMAIN}/api/server-dotnet/JojdaElevator.API'
        sudo dotnet restore
        sudo dotnet build --configuration Release
        
        # 创建systemd服务文件
        sudo tee /etc/systemd/system/${DOMAIN}-api.service > /dev/null <<EOF
[Unit]
Description=${DOMAIN} API Service
After=network.target

[Service]
Type=notify
WorkingDirectory=/var/www/${DOMAIN}/api/server-dotnet/JojdaElevator.API
ExecStart=/usr/bin/dotnet run --configuration Release --urls=http://localhost:5000
Restart=always
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=${DOMAIN}-api
User=www-data

[Install]
WantedBy=multi-user.target
EOF
        
        # 启用并启动服务
        sudo systemctl daemon-reload
        sudo systemctl enable ${DOMAIN}-api
        sudo systemctl restart ${DOMAIN}-api
    "
    
    print_status "后端API部署完成"
fi

# 清理临时文件
ssh "$SERVER_USER@$SERVER_IP" "rm -f /tmp/backend-*.tar.gz /tmp/nginx-*.conf"
rm -f backend-*.tar.gz

# 验证部署
echo "🔍 验证部署状态..."
ssh "$SERVER_USER@$SERVER_IP" "
    # 检查 Nginx 状态
    if sudo systemctl is-active --quiet nginx; then
        echo 'Nginx: ✓ 运行中'
    else
        echo 'Nginx: ✗ 未运行'
    fi
    
    # 检查网站文件
    if [ -f '$REMOTE_WEB_DIR/index.html' ]; then
        echo '网站文件: ✓ 存在'
    else
        echo '网站文件: ✗ 缺失'
    fi
    
    # 检查后端服务（如果存在）
    if sudo systemctl is-active --quiet '${DOMAIN}-api' 2>/dev/null; then
        echo '后端API: ✓ 运行中'
    else
        echo '后端API: - 未配置或未运行'
    fi
"

print_status "部署验证完成"

echo ""
echo "🎉 部署完成！"
echo ""
echo "📋 部署信息："
echo "   域名: https://${DOMAIN}"
echo "   网站目录: ${REMOTE_WEB_DIR}"
echo "   Nginx配置: ${NGINX_CONFIG}"
echo ""
echo "📝 下一步操作："
echo "   1. 确保域名 ${DOMAIN} 的DNS记录指向服务器IP"
echo "   2. 配置SSL证书（推荐使用 Let's Encrypt）"
echo "   3. 测试网站功能是否正常"
echo ""
echo "🔗 快速链接："
echo "   网站: https://${DOMAIN}"
echo "   API: https://${DOMAIN}/api/"
echo ""

# 提示SSL证书配置
print_warning "别忘了配置SSL证书！"
echo "运行以下命令获取免费SSL证书："
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN}" 