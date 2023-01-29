# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['run.py'],
             pathex=[],
             binaries=[],
             datas=[('static', 'static')],
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
          a.binaries,
          a.zipfiles,
          a.datas, 
          [],
          exclude_binaries=True,
          name='Health OCR Digitizer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='static/icon.png')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Health OCR Digitizer')
app = BUNDLE(coll,
             name='Health OCR Digitizer.app',
             icon='static/icon.png',
             bundle_identifier=None)
