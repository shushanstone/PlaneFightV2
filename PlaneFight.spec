# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有游戏资源文件
added_files = [
    ('assets/*.png', 'assets'),
    ('assets/*.wav', 'assets'),
    ('plane_models/*.png', 'plane_models'),
    ('level_config.py', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PlaneFight',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PlaneFight',
)

app = BUNDLE(
    coll,
    name='打飞机游戏.app',
    icon=None,
    bundle_identifier='com.chenxiao.planefight',
    info_plist={
        'CFBundleName': '打飞机游戏',
        'CFBundleDisplayName': '打飞机游戏',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True',
    },
)
