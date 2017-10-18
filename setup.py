#!/usr/bin/python
# -*- coding: utf-8
from setuptools import setup, find_packages

setup(
    name='vatan',
    version='0.1',
    author='Selçuk Karakayalı',
    author_email='skarakayali@gmail.com',
    url='http://github.com/karakays/vatan/',
    packages=find_packages(),
    license='GNU GENERAL PUBLIC LICENSE',
    entry_points={
        'console_scripts': [
            'vatan = vatan.__main__:main'
            ]
    }
)
