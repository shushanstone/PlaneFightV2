@echo off
REM 打飞机游戏 - Windows自动打包脚本
REM 编码: UTF-8

echo ======================================
echo   打飞机游戏 - Windows自动打包工具
echo ======================================
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 检查PyInstaller是否已安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ PyInstaller未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装成功
) else (
    echo ✅ PyInstaller已安装
)

echo.
echo 📦 开始打包游戏...
echo.

REM 清理之前的打包文件
if exist build (
    echo 🧹 清理旧的build目录...
    rmdir /s /q build
)

if exist dist (
    echo 🧹 清理旧的dist目录...
    rmdir /s /q dist
)

REM 执行打包
echo ⚙️  正在打包，这可能需要几分钟时间...
echo.

pyinstaller PlaneFight_Windows.spec --clean

REM 检查打包是否成功
if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo   ✅ 打包成功！
    echo ======================================
    echo.
    echo 📁 可执行文件位置: dist\打飞机游戏.exe
    echo.
    echo 📤 分发说明：
    echo   1. 将 dist\打飞机游戏.exe 发送给朋友
    echo   2. 朋友双击即可运行（无需安装Python）
    echo   3. 首次运行可能被Windows Defender拦截
    echo   4. 选择"仍要运行"即可
    echo.
    echo 💡 提示：
    echo   - 可执行文件大小约 30-40MB
    echo   - 可以压缩成.zip再发送
    echo   - 仅适用于 Windows 7/10/11 系统
    echo.
    
    REM 自动打开dist目录
    explorer dist
) else (
    echo.
    echo ======================================
    echo   ❌ 打包失败
    echo ======================================
    echo.
    echo 请检查以上错误信息
)

pause
