#!/usr/bin/env python
# coding: utf-8
import sys
from setuptools import setup


conditional_kwargs = {'install_requires': ['redis'], 'tests_require': ['pytest>=2.5.0']}

if not hasattr(sys, 'pypy_translation_info'):
    conditional_kwargs['install_requires'].append('ujson')

if sys.version_info < (3, 3):
    conditional_kwargs['tests_require'].append('mock')

setup(
    name='rlog',
    version='0.2',
    description='Small handler and formatter for using python logging with Redis',
    url='https://github.com/lobziik/rlog',
    packages=['rlog', 'tests'],
    license='MIT',
    keywords=['Redis', 'logging', 'log', 'logs'],
    author="lobziik",
    author_email="lobziiko.o@gmail.com",
    maintainer="lobziik",
    maintainer_email="lobziiko.o@gmail.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    **conditional_kwargs
)
