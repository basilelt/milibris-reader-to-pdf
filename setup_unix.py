from setuptools import setup

setup(
    name='MilibrisReaderToPDF',
    version='1.0.0',
    packages=['src'],
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