# app.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],  # This should include the current directory
    binaries=[],
    datas=[
        ('assets/frame0/*', 'assets/frame0'),  # Include assets directory
        ('credentials.json', '.'),  # Include credentials file
        ('config.ini', '.'),  # Include config file if needed
        ('assets/logo.ico', 'assets')  # Include the logo icon
    ],
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
    exclude_binaries=False,  # Ensure binaries are not excluded
    name='DownloadGod',  # Set the application name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='assets/logo.ico'  # Set the application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DownloadGod',
)
