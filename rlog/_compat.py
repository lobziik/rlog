# coding: utf-8
import sys


if sys.version_info[0] == 2:
    text_type = unicode
else:
    text_type = str

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

try:
    import ujson as json
except ImportError:
    import json
