# coding: utf-8
import logging
import sys
import getpass
from datetime import datetime
from socket import gethostname

import ujson as json


if sys.version_info[0] >= 3:
    unicode = str  # python 3 not have unicode


class JSONFormatter(logging.Formatter):

    def format(self, record):
        data = record.__dict__.copy()

        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg

        data.update(
            username=getpass.getuser(),
            time=datetime.now(),
            host=gethostname(),
            message=msg,
            args=tuple(unicode(arg) for arg in record.args)
        )

        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])

        return json.dumps(data)
