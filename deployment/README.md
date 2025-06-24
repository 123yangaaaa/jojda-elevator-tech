# joj达电梯科技 - 部署到 ailingjing.cn 域名

## 🚀 快速部署指南

本文档将指导您将 joj达电梯科技网站部署到 ailingjing.cn 域名。

## 📋 前提条件

### 服务器要求
- Ubuntu 20.04+ 或 CentOS 8+
- 最少 2GB RAM
- 最少 20GB 硬盘空间
- 已安装 Nginx、Node.js、.NET 8.0
- SSH 访问权限

### 域名要求
- 拥有 ailingjing.cn 域名的管理权限
- DNS 记录可以修改
- 建议配置 SSL 证书

### 本地环境
- Git
- Node.js 18+
- SSH 客户端

## 🛠 部署方法

### 方法一：自动脚本部署（推荐）

1. **配置部署参数**
   ```bash
   # 复制环境变量文件
   cp deployment/env.example deployment/.env
   
   # 编辑配置文件
   nano deployment/.env
   ```

2. **修改部署脚本中的服务器信息**
   ```bash
   # 编辑部署脚本
   nano deployment/deploy.sh
   
   # 修改以下变量：
   SERVER_USER="your_username"
   SERVER_IP="your_server_ip"
   ```

3. **运行部署脚本**
   ```bash
   # 给脚本执行权限
   chmod +x deployment/deploy.sh
   
   # 执行部署
   ./deployment/deploy.sh
   ```

### 方法二：Docker 部署

1. **安装 Docker 和 Docker Compose**
   ```bash
   # Ubuntu
   sudo apt update
   sudo apt install docker.io docker-compose
   
   # 启动 Docker
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

2. **配置环境变量**
   ```bash
   cp deployment/env.example deployment/.env
   # 编辑 .env 文件设置数据库密码等
   ```

3. **构建和启动服务**
   ```bash
   cd deployment
   docker-compose up -d --build
   ```

### 方法三：手动部署

1. **构建前端应用**
   ```bash
   npm run build
   ```

2. **上传到服务器**
   ```bash
   scp -r build/* user@server:/var/www/ailingjing.cn/html/
   ```

3. **配置 Nginx**
   ```bash
   scp deployment/nginx.conf user@server:/etc/nginx/sites-available/ailingjing.cn
   ssh user@server "sudo ln -s /etc/nginx/sites-available/ailingjing.cn /etc/nginx/sites-enabled/"
   ssh user@server "sudo nginx -t && sudo systemctl reload nginx"
   ```

## 🔧 配置说明

### Nginx 配置特性
- ✅ HTTP/2 和 SSL 支持
- ✅ Gzip 压缩
- ✅ 静态资源缓存
- ✅ React Router SPA 支持
- ✅ API 反向代理
- ✅ 安全头部设置

### 后端 API 配置
- 端口：5000
- 数据库：MySQL 8.0
- 缓存：Redis（可选）
- 日志：结构化日志记录

## 🌐 DNS 配置

确保以下 DNS 记录指向您的服务器 IP：

```
类型    名称                 值
A       ailingjing.cn       your_server_ip
A       www.ailingjing.cn   your_server_ip
CNAME   api.ailingjing.cn   ailingjing.cn
```

## 🔒 SSL 证书配置

### 使用 Let's Encrypt（免费，推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d ailingjing.cn -d www.ailingjing.cn

# 设置自动续期
sudo crontab -e
# 添加以下行：
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 使用自定义证书

1. 将证书文件放在服务器上：
   ```
   /etc/ssl/certs/ailingjing.cn.crt
   /etc/ssl/private/ailingjing.cn.key
   ```

2. 修改 Nginx 配置中的证书路径

## 📊 监控和维护

### 健康检查
```bash
# 检查网站状态
curl -I https://ailingjing.cn

# 检查 API 状态
curl https://ailingjing.cn/api/health

# 检查服务状态
sudo systemctl status nginx
sudo systemctl status ailingjing.cn-api
```

### 日志查看
```bash
# Nginx 访问日志
sudo tail -f /var/log/nginx/ailingjing.cn.access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/ailingjing.cn.error.log

# API 应用日志
sudo journalctl -f -u ailingjing.cn-api
```

### 备份策略
```bash
# 网站文件备份
sudo tar -czf website-backup-$(date +%Y%m%d).tar.gz /var/www/ailingjing.cn/

# 数据库备份
mysqldump -u root -p JojdaElevatorDB > db-backup-$(date +%Y%m%d).sql
```

## 🔧 故障排除

### 常见问题

1. **网站无法访问**
   - 检查 DNS 解析
   - 检查防火墙设置
   - 检查 Nginx 状态

2. **API 错误**
   - 检查后端服务状态
   - 查看应用日志
   - 验证数据库连接

3. **SSL 证书问题**
   - 验证证书有效期
   - 检查证书文件路径
   - 重新获取证书

### 性能优化

1. **启用 HTTP/2**
   ```nginx
   listen 443 ssl http2;
   ```

2. **配置缓存**
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **启用 Gzip 压缩**
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/javascript;
   ```

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 检查服务器日志
2. 验证配置文件语法
3. 确认网络连接
4. 查看防火墙设置

## 🔄 更新部署

当代码更新时，重新运行部署脚本：

```bash
# 拉取最新代码
git pull origin main

# 重新构建
npm run build

# 重新部署
./deployment/deploy.sh
```

---

## 📝 部署检查清单

- [ ] 服务器环境准备完成
- [ ] 域名 DNS 配置正确
- [ ] SSL 证书配置完成
- [ ] 网站可以正常访问
- [ ] API 接口测试通过
- [ ] 数据库连接正常
- [ ] 静态资源加载正常
- [ ] 移动端适配正常
- [ ] 搜索引擎优化配置
- [ ] 监控和报警配置
- [ ] 备份策略实施 