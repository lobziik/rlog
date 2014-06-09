#!/usr/bin/env python
# coding: utf-8
import sys
from setuptools import setup


setup(
    name='rlog',
    version='0.0.1',
    description='Small handler and formatter for using python logging with Redis',
    url='https://github.com/lobziik/rlog',
    tests_require=['pytest>=2.5.0', 'mock'],
    install_requires=['redis', 'ujson'],
    packages=['rlog', 'tests'],
)
