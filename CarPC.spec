# -*- mode: python -*-

import sys
import os
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    f_path = os.path.join(base_path, relative_path)
    print(f_path)
    return f_path

block_cipher = None

added_files = [
           (resource_path('configs/pids.ini'), 'configs'),
           (resource_path('fonts/RobotoMono.ttf')  , 'fonts'),
           (resource_path('images') , 'images'),
           (resource_path('car.ini'), '.'),
           (resource_path('car.kv') , '.')
]

a = Analysis(['/home/shark/Develop/Projects/R3C/main.py'],
             pathex = ['/home/shark/Develop/Projects/R3C'],
             binaries = None,
             datas = added_files,
             hookspath = [],
             runtime_hooks = [],
             win_no_prefer_redirects = False,
             win_private_assemblies = False,
             cipher = block_cipher,
             **get_deps_all())

pyz = PYZ(a.pure, a.zipped_data, cipher = block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name = 'CarPC',
          debug = False,
          strip = False,
          upx = True,
          console = False )

coll = COLLECT(exe, Tree('/home/shark/Develop/Projects/R3C'),
               a.binaries,
               a.zipfiles:,
               a.datas,
               strip=None,
               upx=True,
               name='CarApp')

