#!/bin/bash
# 打飞机游戏 - 自动打包脚本

echo "======================================"
echo "  打飞机游戏 - 自动打包工具"
echo "======================================"
echo ""

# 检查PyInstaller是否已安装
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller未安装，正在安装..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ PyInstaller安装失败，请手动安装: pip3 install pyinstaller"
        exit 1
    fi
    echo "✅ PyInstaller安装成功"
else
    echo "✅ PyInstaller已安装"
fi

echo ""
echo "📦 开始打包游戏..."
echo ""

# 清理之前的打包文件
if [ -d "build" ]; then
    echo "🧹 清理旧的build目录..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "🧹 清理旧的dist目录..."
    rm -rf dist
fi

# 执行打包
echo "⚙️  正在打包，这可能需要几分钟时间..."
echo ""

pyinstaller PlaneFight.spec --clean

# 检查打包是否成功
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "  ✅ 打包成功！"
    echo "======================================"
    echo ""
    echo "📁 应用程序位置: dist/打飞机游戏.app"
    echo ""
    echo "📤 分发说明："
    echo "  1. 将 dist/打飞机游戏.app 发送给您的朋友"
    echo "  2. 朋友双击即可运行（无需安装Python）"
    echo "  3. 首次打开可能需要右键点击->打开（macOS安全限制）"
    echo ""
    echo "💡 提示："
    echo "  - 应用程序大小约 100-150MB"
    echo "  - 可以压缩成.zip再发送"
    echo "  - 仅适用于 macOS 系统"
    echo ""
else
    echo ""
    echo "======================================"
    echo "  ❌ 打包失败"
    echo "======================================"
    echo ""
    echo "请检查以上错误信息"
    exit 1
fi
