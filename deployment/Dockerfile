# joj达电梯科技 - 多阶段Docker构建

# 第一阶段：构建 React 应用
FROM node:18-alpine AS build

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 第二阶段：Nginx 服务器
FROM nginx:1.25-alpine

# 安装必要工具
RUN apk add --no-cache curl

# 删除默认 nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义 nginx 配置
COPY deployment/nginx-docker.conf /etc/nginx/conf.d/

# 复制构建的文件到 nginx html 目录
COPY --from=build /app/build /usr/share/nginx/html

# 复制 SSL 证书（如果有）
# COPY deployment/ssl/ /etc/ssl/

# 设置正确的权限
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# 暴露端口
EXPOSE 80 443

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"] 