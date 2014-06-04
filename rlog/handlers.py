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


class RedisListHandler(logging.Handler):

    def __init__(self, key, max_messages, redis_client=None, host='localhost', port=6379,
                 password=None, db=0, level=logging.NOTSET):
        """
        Create a new logger for the given key and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.key = key
        self.redis_client = redis_client or redis.Redis(host=host, port=port, password=password, db=db)
        self.formatter = JSONFormatter()
        self.max_messages = max_messages

    def emit(self, record):
        """
        Publish record to redis logging list
        """
        try:
            if self.max_messages:
                p = self.redis_client.pipeline()
                p.rpush(self.key, self.format(record))
                p.ltrim(self.key, -self.max_messages, -1)
                p.execute()
            else:
                self.redis_client.rpush(self.key, self.format(record))
        except redis.RedisError:
            pass
