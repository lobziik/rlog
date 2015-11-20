# coding: utf-8
import logging
import redis
import time

from rlog import RedisHandler
from rlog import RedisListHandler
from rlog._compat import json, patch, Mock


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


def test_log_publish_custom_formatter(clean_logger):
    logger = clean_logger
    logger.addHandler(RedisHandler(
        channel='test',
        formatter=logging.Formatter(
            '%(asctime)s|%(name)s|%(levelname)s|%(message)s')))

    redis_client = redis.Redis()
    p = redis_client.pubsub()
    p.subscribe('test')

    logger.warn('test')

    message = wait_for_message(p, 1, True)['data']

    ts, name, levelname, msg = message.split(b'|')
    assert levelname == b'WARNING'
    assert msg == b'test'


def test_log_list_rotator():
    logger = logging.getLogger()
    logger.addHandler(
        RedisListHandler(
            key='test', max_messages=2, redis_client=redis.Redis(db=1)))

    redis_client = redis.Redis(db=1)
    redis_client.delete('test')

    logger.warn('test')
    p = redis_client.pipeline()
    p.lrange('test', 0, -1)
    data = p.execute()[0]
    assert len(data) == 1


def test_redis_emit_error(redis_logger):
    handler = redis_logger.handlers[0]
    with patch.object(handler.redis_client, 'publish') as mock_publish:
        mock_publish.side_effect = redis.RedisError()
        redis_logger.warn('test2')


def test_redis_list_emit_error():
    logger = logging.getLogger()
    handler = RedisListHandler(
        key='test', max_messages=2, redis_client=redis.Redis(db=1))
    handler.redis_client.pipeline = Mock(side_effect=redis.RedisError())
    logger.addHandler(handler)
    logger.warn('test')


def test_redis_list_ttl_not_expired(clean_logger):
    logger = clean_logger
    handler = RedisListHandler(key='test', ttl=60)
    logger.addHandler(handler)
    logger.warn('test')

    redis_client = redis.Redis()
    p = redis_client.pipeline()
    p.lrange('test', 0, -1)
    data = p.execute()[0]
    assert len(data) == 1


def test_redis_list_ttl_expired(clean_logger):
    logger = clean_logger
    handler = RedisListHandler(key='test', ttl=1)
    logger.addHandler(handler)
    logger.warn('test')

    time.sleep(2)

    redis_client = redis.Redis()
    p = redis_client.pipeline()
    p.lrange('test', 0, -1)
    data = p.execute()[0]
    assert len(data) == 0
