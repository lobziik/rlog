# coding: utf-8
import logging
import ujson as json

from rlog.formatters import JSONFormatter


def test_formatter():
    record = logging.makeLogRecord({})
    formatter = JSONFormatter()
    formatted_record = formatter.format(record)
    data = json.loads(formatted_record)
    assert data

