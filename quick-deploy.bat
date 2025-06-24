@echo off
chcp 65001 >nul
echo 🚀 joj达电梯科技 - 快速部署到 ailingjing.cn
echo.

:: 检查是否存在 build 目录
if not exist "build" (
    echo 📦 开始构建生产版本...
    call npm run build
    if errorlevel 1 (
        echo ❌ 构建失败！
        pause
        exit /b 1
    )
    echo ✅ 构建完成！
    echo.
)

:: 检查部署配置
if not exist "deployment\.env" (
    if exist "deployment\env.example" (
        echo 📋 复制环境变量配置文件...
        copy "deployment\env.example" "deployment\.env"
        echo.
        echo ⚠️  请编辑 deployment\.env 文件配置服务器信息后重新运行此脚本
        echo.
        pause
        exit /b 1
    )
)

echo 📋 部署选项：
echo 1. 自动脚本部署（需要配置服务器信息）
echo 2. 生成 Docker 镜像
echo 3. 仅构建文件（手动部署）
echo 4. 查看部署文档
echo.

set /p choice="请选择部署方式 (1-4): "

if "%choice%"=="1" goto auto_deploy
if "%choice%"=="2" goto docker_deploy
if "%choice%"=="3" goto manual_build
if "%choice%"=="4" goto show_docs
goto invalid_choice

:auto_deploy
echo.
echo 🔧 开始自动部署...
echo ⚠️  注意：请确保已在 deployment\.env 中配置正确的服务器信息
echo.
set /p confirm="确认继续？(y/N): "
if /i not "%confirm%"=="y" goto end

echo 📤 执行部署脚本...
:: 在 Windows 下使用 Git Bash 或 WSL 执行 shell 脚本
where bash >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 bash。请安装 Git for Windows 或 WSL
    echo 💡 或者使用 Docker 部署方式
    goto end
)

bash deployment/deploy.sh
goto end

:docker_deploy
echo.
echo 🐳 生成 Docker 镜像...
where docker >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Docker。请先安装 Docker Desktop
    goto end
)

echo 📦 构建 Docker 镜像...
docker build -f deployment/Dockerfile -t jojda-elevator:latest .
if errorlevel 1 (
    echo ❌ Docker 镜像构建失败！
    goto end
)

echo ✅ Docker 镜像构建完成！
echo.
echo 🚀 启动容器选项：
echo 1. 启动单个前端容器
echo 2. 启动完整应用栈（包括数据库）
echo.

set /p docker_choice="请选择启动方式 (1-2): "
if "%docker_choice%"=="1" (
    echo 📤 启动前端容器...
    docker run -d -p 80:80 --name jojda-frontend jojda-elevator:latest
    echo ✅ 前端容器已启动，访问 http://localhost
) else if "%docker_choice%"=="2" (
    echo 📤 启动完整应用栈...
    cd deployment
    docker-compose up -d
    cd ..
    echo ✅ 完整应用栈已启动
)
goto end

:manual_build
echo.
echo 📁 构建文件已生成在 build/ 目录中
echo.
echo 📋 手动部署步骤：
echo 1. 将 build/ 目录下的文件上传到服务器 /var/www/ailingjing.cn/html/
echo 2. 配置 Nginx（参考 deployment/nginx.conf）
echo 3. 配置 SSL 证书
echo 4. 重启 Nginx 服务
echo.
echo 📖 详细说明请查看 deployment/README.md
goto end

:show_docs
echo.
echo 📖 正在打开部署文档...
start deployment/README.md
goto end

:invalid_choice
echo ❌ 无效选择，请重新运行脚本
goto end

:end
echo.
echo 🎉 操作完成！
echo.
echo 📋 有用链接：
echo - 部署文档: deployment/README.md
echo - Nginx配置: deployment/nginx.conf
echo - Docker配置: deployment/docker-compose.yml
echo.
pause 