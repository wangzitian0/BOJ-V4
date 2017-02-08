import nsq
import time
import requests
import json
import django

import socket
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bojv4.settings'
django.setup()
from django.contrib.auth.models import User
from submission.models import Submission
from contest.models import Contest
from common.redis import redisClient
from django.shortcuts import get_object_or_404
import time

def handler(message):
    print message
    mp = json.loads(message.body)
    print mp
    s_pk = int(mp['submission_pk'])
    print s_pk
    try:
        s = Submission.objects.get(pk=s_pk)
        if s.isContest:
           redisClient.sadd 
        s.save()
        print "======="
    except Exception, ex:
        print ex
    return {'status': 'OK', 'reason': r.text}

r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=['127.0.0.1:4150'],
        topic='submission', channel='asdfxx', lookupd_poll_interval=15)

nsq.run()
