# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['connect.py'],
             pathex=['C:/Users/kaito/Projects/flowSound/src'],
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
a.datas += [('static/ui_files/fin.ui', './static/ui_files/fin.ui', 'DATA'),
            ('static/ui_files/guide.ui', './static/ui_files/guide.ui', 'DATA'),
            ('static/ui_files/menu.ui', './static/ui_files/menu.ui', 'DATA'),
            ('static/ui_files/result.ui', './static/ui_files/result.ui', 'DATA'),
            ('static/ui_files/settings.ui', './static/ui_files/settings.ui', 'DATA'),
            ('static/ui_files/test.ui', './static/ui_files/test.ui', 'DATA'),
            ]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
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
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='prototype')
