# coding: utf-8
import logging
from rlog.handlers import RedisListHandler
import ujson as json
import time
import redis


def wait_for_message(pubsub, timeout=0.1, ignore_subscribe_messages=False):
    now = time.time()
    timeout = now + timeout
    while now < timeout:
        message = pubsub.get_message(
            ignore_subscribe_messages=ignore_subscribe_messages)
        if message is not None:
            return message
        time.sleep(0.01)
        now = time.time()
    return None


def test_log_publish(redis_logger):

    redis_client = redis.Redis()
    p = redis_client.pubsub()
    p.subscribe('test')

    redis_logger.warn('test')

    message = json.loads(wait_for_message(p, 1, True)['data'])

    assert 'levelname' in message
    assert 'msg' in message
    assert message['levelname'] == 'WARNING'
    assert message['msg'] == 'test'


def test_log_list_rotator():
    logger = logging.getLogger()
    logger.addHandler(RedisListHandler(key='test', db=1, max_messages=2))

    redis_client = redis.Redis(db=1)
    redis_client.delete('test')

    logger.warn('test')
    p = redis_client.pipeline()
    p.lrange('test', 0, -1)
    data = p.execute()[0]
    assert len(data) == 1
