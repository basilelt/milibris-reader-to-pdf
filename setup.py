"""
setup.py - Build script for Milibris Reader to PDF application.

This script configures the build process for creating a standalone macOS application
that converts Milibris Reader HTML files to PDF format. It uses py2app to bundle
the Python application into a native macOS .app package.

Dependencies:
    - PyQt6: For the graphical user interface
    - img2pdf: For PDF conversion functionality
    - py2app: For macOS application bundling

Original work by Fabrice Aeschbacher
Modified by BasileLT
License: MIT
"""

from setuptools import setup

APP = ['src/gui.py']
DATA_FILES = ['src/app_icon.icns']
OPTIONS = {
    'argv_emulation': False,
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
