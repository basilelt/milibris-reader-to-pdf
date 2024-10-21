from setuptools import setup

APP = ['src/gui.py']
DATA_FILES = ['src/gen-pdf.py', 'src/app_icon.icns']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6', 'img2pdf'],
    'includes': ['subprocess', 'mmap', 'urllib', 'shutil'],
    'excludes': ['packaging'],
    'iconfile': 'src/app_icon.icns',
    'plist': {
        'CFBundleName': 'Milibris Reader to PDF',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.basilelt.milibrisreader',
    },
}

setup(
    app=APP,
    name='Milibris Reader to PDF',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['PyQt6', 'img2pdf'],
)