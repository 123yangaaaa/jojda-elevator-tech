@echo off
echo ========================================
echo    joj达电梯产品查找器演示系统启动
echo ========================================
echo.

echo [1/3] 检查依赖项...
if not exist "node_modules" (
    echo 正在安装前端依赖...
    call npm install
)

if not exist "server/node_modules" (
    echo 正在安装后端依赖...
    cd server
    call npm install
    cd ..
)

echo.
echo [2/3] 启动后端服务器...
start "后端服务器" cmd /k "cd server && npm start"

echo 等待后端服务器启动...
timeout /t 3 /nobreak >nul

echo.
echo [3/3] 启动前端应用...
echo 正在启动React开发服务器...
echo.
echo ========================================
echo  系统启动完成！
echo  前端地址: http://localhost:3000
echo  后端地址: http://localhost:5000
echo  点击"Knowledge Orbs"按钮体验产品查找器
echo ========================================
echo.

call npm start 