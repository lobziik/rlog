# coding: utf-8
import pytest
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
    p = redis_client.pubsub(ignore_subscribe_messages=True)
    p.subscribe('test')

    redis_logger.warn('test')

    message = json.loads(wait_for_message(p, 1, True)['data'])

    assert 'levelname' in message
    assert 'msg' in message
    assert message['levelname'] == 'WARNING'
    assert message['msg'] == 'test'




