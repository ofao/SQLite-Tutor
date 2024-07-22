# -*- mode: python ; coding: utf-8 -*-
import os
from os.path import join

from kivy import kivy_data_dir
from kivy_deps import sdl2, glew
from kivy.tools.packaging import pyinstaller_hooks as hooks

block_cipher = None
kivy_deps_all = hooks.get_deps_all()
kivy_factory_modules = hooks.get_factory_modules()

datas = [
    (join('1', '*.*'), '1'),
     (join('2', '*.*'), '2'),
     (join('3', '*.*'), '3'),
     (join('4', '*.*'), '4'),
     (join('5', '*.*'), '5'),
     (join('6', '*.*'), '6'),
     (join('7', '*.*'), '7'),
     ('data.json', '.'),
     ('sq.db', '.'),
     ('*.png', '.'),
     ('*.jpg', '.')    
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='SQLiteTutor',
    icon='database.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(exe, Tree('C:\\Users\\Acer\\Desktop\\mobile'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='SQLiteTutor')
