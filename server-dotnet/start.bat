@echo off
echo ========================================
echo    joj达电梯科技 .NET API 服务启动
echo ========================================
echo.

cd /d "%~dp0JojdaElevator.API"

echo 正在检查 .NET SDK...
dotnet --version
if %ERRORLEVEL% neq 0 (
    echo 错误: 未找到 .NET SDK，请先安装 .NET 8.0 SDK
    pause
    exit /b 1
)

echo.
echo 正在还原 NuGet 包...
dotnet restore
if %ERRORLEVEL% neq 0 (
    echo 错误: NuGet 包还原失败
    pause
    exit /b 1
)

echo.
echo 正在构建项目...
dotnet build
if %ERRORLEVEL% neq 0 (
    echo 错误: 项目构建失败
    pause
    exit /b 1
)

echo.
echo 正在启动 API 服务...
echo 服务地址: https://localhost:7000
echo Swagger UI: https://localhost:7000
echo.
echo 按 Ctrl+C 停止服务
echo.

dotnet run

pause 