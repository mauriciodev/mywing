# -*- mode: python -*-
import os

def Datafiles(*filenames, **kw):

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

uifiles=Datafiles('Qt/addPilotDialog.ui', 'Qt/battleViewerDialog.ui', 'Qt/pilotCard.ui')
jsonfiles = Datafiles('data/pilots.json','data/moves.json','data/ships.json')
imagefiles = Datafiles('images/nave1.png','images/nave2.png','images/scenarios/maxresdefault.jpg','images/tokens.svg')

a = Analysis(['myWing.py'],
             pathex=['C:\\Documents and Settings\\vatto\\Desktop\\mywing-master'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='myWing.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
			   jsonfiles,
			   uifiles,
			   imagefiles,
               strip=None,
               upx=True,
               name='myWing')
