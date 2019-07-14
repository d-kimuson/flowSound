from distutils.core import setup
import py2exe


option = {
    'bundle_files': 1,
    'compressed': False
}
setup(
    options={'py2exe': option},
    console=['connect.py'],
    zipfile='Prototype.zip',
    )
