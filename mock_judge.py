import nsq
import time
import requests
import json
from datetime import datetime
import threading
import multiprocessing
import nsq


def handler(message):
    print "start judge"
    url = "http://127.0.0.1:4151/put?topic=submission"
    cnt = 3
    mp = json.loads(message.body)
    r = requests.post(url, data=json.dumps({
        "submission-id": mp['submission_id'],
        "status": 'AC',
    }))
    print r.text
    if r.text == 'OK':
        return {'status': 'OK', 'msg': 'success'}
    return {'status': 'Failed', 'reason': r.text}


if __name__ == '__main__':
    # NsqQueue.add_callback(handler=cheat_handler, topic='cheat', channel='adfasdf')
    r = nsq.Reader(message_handler=handler, lookupd_http_addresses=['http://127.0.0.1:4161'],
            topic='judge', channel='abcdefg', lookupd_poll_interval=15)

    nsq.run()
