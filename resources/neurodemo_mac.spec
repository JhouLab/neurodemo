# -*- mode: python ; coding: utf-8 -*-

added_files = [
    ( '../neurodemo/images/channel.svg', 'images' ),
    ( '../neurodemo/images/channel2.svg', 'images' ),
    ( '../neurodemo/images/cell.svg', 'images' ),
    ( '../neurodemo/images/pipette.svg', 'images' ),
    # Lands in Contents/Resources, where Qt reads it during QtCore's static
    # initializers. Without it, Qt resolves its paths via CFBundle APIs, which
    # segfault in this bundle layout before Python can run.
    ( 'qt.conf', '.' ),
]

a = Analysis(
    ['../neurodemo.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[ 'PyQt6.QtSvgWidgets' ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='neurodemo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='neurodemo',
)

app = BUNDLE(
    coll,
    name='neurodemo.app',
    icon='icon.icns',
    bundle_identifier=None,
)
