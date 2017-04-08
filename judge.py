import os
import sys
import django
import nsq
import json
import requests
from bojv4 import conf
import time
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bojv4.settings'
django.setup()

from submission.models import Submission, CaseResult


class NsqQueue(object):

    handlers = []

    @classmethod
    def add_callback(cls, handler, topic, channel, address='127.0.0.1:4150'):
        r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=[address],
                topic=topic, channel=channel, lookupd_poll_interval=15)
        cls.handlers.append(r)

    @classmethod
    def start(cls):
        nsq.run()


def submission_handler(message):
    try:
        mp = json.loads(message.body)
        print mp
        sub_pk = mp.get('submission-id', None)
        sub = Submission.objects.filter(pk=sub_pk).first()
        status = mp.get('status', None)
        if not status or status not in conf.STATUS_CODE.keys():
            return True
        position = mp.get('position', None)
        if position:
            CaseResult.deal_case_result(mp)
        elif not position or status != 'AC':
            sub.status = status
            # sub.status = result.get('status', 'JD')
        sub.running_time = mp.get('running_time', 0)
        sub.running_memory = mp.get('running_memory', 0)
        sub.save()
    except Exception as ex:
        print ex
    return True


def cheat_handler(message):
    print 'cheat=================',  message.body
    return True


if __name__ == '__main__':
    NsqQueue.add_callback(handler=submission_handler, topic='submission', channel='123456')
    NsqQueue.add_callback(handler=cheat_handler, topic='cheat', channel='adfasdf')
    NsqQueue.start()


