# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

options = [ ('u', None, 'OPTION') ]
a = Analysis(['C:\\path-to-solution-root\\SomUI\\scripts\\data_preparation_interactive.py', 'data_preparation_interactive.spec'],
             pathex=['C:\\path-to-python-root'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          options,
          exclude_binaries=True,
          name='data_preparation_interactive',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='data_preparation_interactive')
