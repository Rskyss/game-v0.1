from setuptools import setup

APP = ['server.py']  # 你的主脚本文件
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)