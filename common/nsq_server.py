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
from django.shortcuts import get_object_or_404
from common.redis_client import calc_contest_score
import time

def handler(message):
    print message
    mp = json.loads(message.body)
    print mp
    s_pk = int(mp['submission_pk'])
    print s_pk
    try:
        s = Submission.objects.get(pk=s_pk)
        s.status = mp.get('status', 'SE')
        s.running_time = mp.get('running_time', 0)
        s.running_memery = mp.get('running_memory', 0)
        if s.status == 'CE':
            s.set_info('CE_REASON', mp.get('CE_REASON', ''))
        else if s.status != 'JD':
            info = json.loads(s.info)
            if not info or info == '':
                info = {}
            for res in mp.get('case_result'):
                info[res['index']] = res['result']
            s.info = json.dumps(info)
        s.save()
        calc_contest_score(s)
    except Exception, ex:
        print ex
    return {'status': 'OK', 'reason': r.text}

r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=['127.0.0.1:4150'],
        topic='submission', channel='asdfxx', lookupd_poll_interval=15)

nsq.run()
