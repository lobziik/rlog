# coding: utf-8
import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = hasattr(sys, 'pypy_translation_info')


if PY2:
    text_type = unicode
else:
    text_type = str

try:
    import ujson as json
except ImportError:
    import json
