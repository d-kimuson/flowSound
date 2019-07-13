# -*- mode: python -*-

block_cipher = None


a = Analysis(['connect.py'],
             pathex=['/Users/kaito/Apps/flowSound/exe'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(Tree('../src/static/', prefix='static/'),
          pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='connect',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='Prototype.app',
             info_plist={ 'NSHighResolutionCapable': 'True'},
             icon=None,
             bundle_identifier=None)
