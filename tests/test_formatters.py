# coding: utf-8
import logging
import ujson as json
import sys

from rlog.formatters import JSONFormatter


def get_result_record(**kwargs):
    record = logging.makeLogRecord(kwargs)
    formatter = JSONFormatter()
    formatted_record = formatter.format(record)
    return json.loads(formatted_record)


def test_formatter():
    data = get_result_record(msg='Test %s', args=('format', ))
    assert data['message'] == 'Test format'


def test_exception_info():
    try:
        1 / 0
    except ZeroDivisionError:
        data = get_result_record(exc_info=sys.exc_info())
        if sys.version_info[0] >= 3:
            assert 'ZeroDivisionError: division by zero' in data['exc_info']
        else:
            assert 'ZeroDivisionError: division or modulo by zero' in data['exc_info']
