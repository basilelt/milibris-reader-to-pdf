"""
setup_unix.py - Unix build configuration for Milibris Reader to PDF

This script configures the build process for Unix systems (Linux/macOS) to create
an installable Python package that converts Milibris Reader HTML files to PDF format.

Dependencies:
    - PyQt6: GUI framework
    - img2pdf: PDF conversion library

Original work by Fabrice Aeschbacher
Modified by BasileLT
License: MIT
"""

from setuptools import setup

setup(
    name='MilibrisReaderToPDF',
    version='1.0.0',
    packages=['src'],
    package_data={
        'src': ['gen_pdf.py', 'app_icon.icns']
    },
    install_requires=[
        'PyQt6',
        'img2pdf',
    ],
    entry_points={
        'console_scripts': [
            'milibris-reader=src.gui:main',
        ],
    },
    python_requires='>=3.8',
)
