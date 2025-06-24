@echo off
chcp 65001 >nul
echo ========================================
echo    奥的斯电梯产品图自动下载器
echo ========================================
echo.
echo 请选择要运行的下载器:
echo.
echo 1. 增强版自动下载器 (单个产品)
echo 2. 批量下载器 (多个产品)
echo 3. 基础版分析器 (仅分析网站)
echo.
set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 启动增强版自动下载器...
    python enhanced_auto_downloader.py
) else if "%choice%"=="2" (
    echo.
    echo 启动批量下载器...
    python batch_downloader.py
) else if "%choice%"=="3" (
    echo.
    echo 启动基础版分析器...
    python auto_downloader.py
) else (
    echo.
    echo 无效的选择！
    pause
    exit /b 1
)

echo.
echo 程序执行完成！
pause 