import nsq
import time
import requests
import json
def handler(message):
    time.sleep(1) 
    print type(message)
    print "===="
    print message.body
    url = "http://127.0.0.1:4151/put?topic=submission"
    cnt = 3
    mp = json.loads(message.body)
    mp['result'] = 'AC'
    while cnt > 0:
        cnt -= 1
        r = requests.post(url, data=json.dumps(mp)) 
        print r.text
        if r.text == 'OK':
            return {'status': 'OK', 'msg': 'success'}
    return {'status': 'Failed', 'reason': r.text}

r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=['127.0.0.1:4150'],
        topic='judge', channel='asdfxx', lookupd_poll_interval=15)

nsq.run()
