# -*- mode: python -*-

from kivy.deps import sdl2,glew

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\pc\\Documents\\GitHub\\Pyweek-25'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='bitetris',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icon.png')

coll = COLLECT(exe, Tree('C:\\Users\\pc\\Documents\\GitHub\\Pyweek-25'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='bitetris')


