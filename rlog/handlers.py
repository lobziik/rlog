# coding: utf-8
import logging
import redis

from .formatters import JSONFormatter


class RedisHandler(logging.Handler):
    """
    Publish messages to redis channel.
    """

    def __init__(self, channel, redis_client=None, host='localhost', port=6379,
                 password=None, db=0, level=logging.NOTSET):
        """
        Create a new logger for the given channel and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.channel = channel
        self.redis_client = redis_client or redis.Redis(host=host, port=port, password=password, db=db)
        self.formatter = JSONFormatter()

    def emit(self, record):
        """
        Publish record to redis logging channel
        """
        try:
            self.redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            pass
