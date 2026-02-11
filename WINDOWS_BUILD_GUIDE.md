# 打飞机游戏 - Windows打包指南

## ⚠️ 重要说明

**您当前使用的是 macOS 系统**，但 PyInstaller **无法在 macOS 上打包 Windows 程序**。

要生成 Windows 的 `.exe` 文件，您需要在 **Windows 系统** 上运行打包命令。

---

## 🎯 三种解决方案

### 方案一：在 Windows 电脑上打包（推荐）

如果您有 Windows 电脑或朋友有 Windows 电脑：

#### 步骤1：将项目复制到 Windows 电脑

将以下文件/文件夹复制到 Windows 电脑：
```
PlaneFightV2/
├── main.py
├── level_config.py
├── requirements.txt
├── PlaneFight_Windows.spec
├── build_windows.bat
├── assets/
└── plane_models/
```

#### 步骤2：在 Windows 上运行打包脚本

1. 双击 `build_windows.bat`
2. 等待打包完成（约2-5分钟）
3. 打包后的文件在 `dist\打飞机游戏.exe`

#### 步骤3：测试和分发

- 双击 `打飞机游戏.exe` 测试
- 可以将这个 exe 文件发送给任何 Windows 用户

---

### 方案二：使用虚拟机

如果您的 Mac 上安装了虚拟机软件：

#### 2.1 使用 Parallels Desktop / VMware Fusion / VirtualBox

1. 在虚拟机中安装 Windows 10/11
2. 在虚拟机中安装 Python 3.7+
3. 将项目文件复制到虚拟机
4. 按照方案一的步骤2执行

#### 2.2 手动打包命令

在 Windows 虚拟机的 PowerShell 或 CMD 中：

```bash
# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 打包
pyinstaller PlaneFight_Windows.spec --clean
```

---

### 方案三：使用 GitHub Actions（自动化，推荐）

使用 GitHub 的免费 CI/CD 服务在云端打包：

#### 步骤1：创建 GitHub 仓库

1. 在 GitHub 上创建新仓库
2. 上传项目文件

#### 步骤2：创建 GitHub Actions 工作流

创建文件 `.github/workflows/build-windows.yml`：

```yaml
name: Build Windows EXE

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        pyinstaller PlaneFight_Windows.spec --clean
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: PlaneFight-Windows
        path: dist/打飞机游戏.exe
```

#### 步骤3：下载打包文件

1. 推送代码到 GitHub
2. GitHub Actions 自动在 Windows 环境中打包
3. 在 Actions 页面下载生成的 exe 文件

---

## 📋 Windows 打包详细步骤（方案一）

### 前置要求

- Windows 7 / 10 / 11
- Python 3.7 或更高版本
- 约 500MB 磁盘空间

### 安装 Python（如果未安装）

1. 访问 https://www.python.org/downloads/
2. 下载 Windows 版本
3. **重要**：安装时勾选 "Add Python to PATH"

### 打包步骤

#### 方法A：使用自动脚本（简单）

1. 双击 `build_windows.bat`
2. 脚本会自动：
   - 检查 Python
   - 安装 PyInstaller
   - 打包游戏
   - 打开 dist 文件夹

#### 方法B：手动打包

打开 PowerShell 或 CMD，执行：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 安装 PyInstaller
pip install pyinstaller

# 3. 打包
pyinstaller PlaneFight_Windows.spec --clean
```

### 打包结果

成功后会生成：
- `dist\打飞机游戏.exe` （约 30-40 MB）

---

## 🎮 Windows 用户如何使用

### 运行游戏

1. 双击 `打飞机游戏.exe`
2. 开始游戏！

### 首次运行可能遇到的问题

#### 问题1：Windows Defender SmartScreen 警告

**提示**："Windows 已保护你的电脑"

**解决**：
1. 点击 "更多信息"
2. 点击 "仍要运行"

#### 问题2：杀毒软件拦截

**原因**：未签名的可执行文件可能被误报

**解决**：
1. 添加到杀毒软件白名单
2. 或暂时禁用杀毒软件

#### 问题3：缺少 DLL 文件

**错误**："无法启动此程序，因为计算机中丢失 VCRUNTIME140.dll"

**解决**：
1. 下载并安装 Microsoft Visual C++ Redistributable
2. 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## 📊 打包对比

| 项目 | macOS (.app) | Windows (.exe) |
|------|-------------|----------------|
| 打包系统 | macOS | Windows |
| 文件大小 | ~37 MB | ~30-40 MB |
| 打包工具 | PyInstaller | PyInstaller |
| 是否需要运行时 | 否 | 否 |
| 跨平台打包 | ❌ | ❌ |

---

## 🔧 配置文件说明

### PlaneFight_Windows.spec

这是 Windows 打包的配置文件，关键设置：

```python
# 单文件模式（所有内容打包到一个exe）
exe = EXE(
    ...
    name='打飞机游戏',
    console=False,  # 不显示控制台
    ...
)
```

**与 macOS 版本的区别**：
- 路径分隔符使用 `\\` 而不是 `/`
- 生成单个 `.exe` 文件而不是 `.app` 包
- 不需要 BUNDLE 配置

---

## 💡 实用建议

### 如果您没有 Windows 电脑

1. **最简单**：请有 Windows 电脑的朋友帮忙打包
2. **云服务**：使用 GitHub Actions（免费）
3. **虚拟机**：在 Mac 上安装 Windows 虚拟机

### 打包后的文件分发

```bash
# 压缩（可选）
# 在 Windows 中右键 -> 发送到 -> 压缩文件
```

### 减小文件大小

如果想要更小的文件：

```python
# 在 .spec 文件中设置
upx=True,  # 使用 UPX 压缩
```

---

## 🎯 快速开始（给您的 Windows 朋友）

把这段说明发给您的 Windows 朋友：

```
嗨！请帮我打包一个 Windows 游戏：

1. 解压我发给你的项目文件夹
2. 双击运行 build_windows.bat
3. 等待打包完成（约2-5分钟）
4. 把 dist 文件夹里的 打飞机游戏.exe 发回给我

就这么简单！谢谢！🙏
```

---

## ❓ 常见问题

### Q: 为什么不能在 Mac 上打包 Windows 程序？

A: PyInstaller 使用的是平台特定的二进制文件和系统库，无法跨平台打包。必须在目标平台上打包。

### Q: 有没有支持跨平台打包的工具？

A: 
- **Nuitka**：可以跨平台，但配置复杂
- **cx_Freeze**：部分支持，但效果不如 PyInstaller
- **GitHub Actions**：最推荐的方案

### Q: exe 文件为什么这么大？

A: 因为打包了 Python 解释器和所有依赖库。这是正常的。

### Q: 能不能打包成安装程序？

A: 可以，打包后使用 Inno Setup 或 NSIS 制作安装程序。

---

## 📝 文件清单

在 Windows 上打包需要这些文件：

```
✅ main.py                      # 主程序
✅ level_config.py              # 关卡配置
✅ requirements.txt             # Python依赖
✅ PlaneFight_Windows.spec      # Windows打包配置
✅ build_windows.bat            # 自动打包脚本
✅ assets/                      # 游戏资源
✅ plane_models/                # 飞机模型
```

---

## 🎉 总结

**现状**：您在 macOS 上，无法直接打包 Windows exe

**解决方案**：
1. ⭐ **推荐**：请 Windows 朋友帮忙打包（最简单）
2. ⭐ **推荐**：使用 GitHub Actions（全自动）
3. 使用虚拟机（需要安装 Windows）

**我已经为您准备好了**：
- ✅ Windows 打包配置文件
- ✅ 自动打包脚本
- ✅ 详细的打包说明

只需在 Windows 电脑上运行即可！

---

**文档版本**: 1.0  
**创建时间**: 2026年2月11日  
**作者**: CodeFlicker AI Assistant
