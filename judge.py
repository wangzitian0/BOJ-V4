import os
import sys
import django
import nsq
import json
import requests
from bojv4 import conf
import time
import threading
from django.db import connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bojv4.settings'
django.setup()

from submission.models import Submission, CaseResult
from contest.models import ContestSubmission, ContestProblem
from django.contrib.auth.models import User
import logging
logger = logging.getLogger('judge')


class NsqQueue(object):

    handlers = []

    @classmethod
    def add_callback(cls, handler, topic, channel, address='http://127.0.0.1:4161'):
        r = nsq.Reader(message_handler=handler, lookupd_http_addresses=[address],
                topic=topic, channel=channel, lookupd_poll_interval=15)
        cls.handlers.append(r)

    @classmethod
    def start(cls):
        nsq.run()


def submission_handler(message):
    logger.info('receive judge result')
    try:
        connection.close()
        mp = json.loads(message.body)
        # print json.dumps(mp, indent=4)
        sub_pk = mp.get('submission-id', None)
        sub = Submission.objects.filter(pk=sub_pk).first()
        status = mp.get('status', None)
        logger.info('receive : ' + str(sub_pk) + status)
        if not sub or not status or status not in conf.STATUS_CODE.keys():
            print conf.STATUS_CODE.keys()
            return True
        position = mp.get('position', '')
        logger.info('receive : ' + str(sub_pk) + str(position))
        if position != '':
            # CaseResult.deal_case_result(mp)
            case = CaseResult()
            case.position = int(position)
            case.submission = sub
            case.running_time = mp.get('time', 0)
            case.running_memory = mp.get('memory', 0)
            case.status = status
            print "============create=========="
            case.save()
            print "============create success, pk is ", case.pk
            if status == 'AC':
                sub.score += sub.problem.get_score(position)
                sub.save()
            sub.deal_case_result(case)
        else:
            if 'compile-message' in mp:
                sub.set_info('compile-message', mp['compile-message'])
            sub.status = status
            sub.save()
        logger.info("judge end")
    except Exception as ex:
        logger.error("judge error: "+str(ex))
        print ex
    return True


def submit_handler(message):
    print 'cheat=================',  message.body
    try:
        mp = json.loads(message.body)
        print mp
        s = ContestSubmission()
        s.problem = ContestProblem.objects.get(pk=int(mp['problem']))
        sub = Submission()
        sub.code = mp['code']
        sub.language = mp['language']
        sub.problem = s.problem.problem
        sub.user = User.objects.get(pk=int(mp['user']))
        sub.save()
        s.submission = sub
        s.save()
        sub.judge()
    except Exception as ex:
        print ex
    return True


if __name__ == '__main__':
    print "start run"
    NsqQueue.add_callback(handler=submission_handler, topic='submission', channel='123456')
    NsqQueue.add_callback(handler=submit_handler, topic='submit', channel='adfasdf')
    print "end add"
    NsqQueue.start()

