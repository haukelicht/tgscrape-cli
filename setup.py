# setup.py
from setuptools import setup

setup(
    name='tgscrape',
    version='0.0.1',
    py_modules=['tgscrape'],
    packages=['custom'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tgscrape=tgscrape:cli
    ''',
)
