import nsq
import time
import requests
import json
from datetime import datetime
import threading
import multiprocessing

def handler(message):
    url = "http://127.0.0.1:4151/put?topic=submission"
    cnt = 3
    while cnt > 0:
        cnt -= 1
        r = requests.post(url, data=json.dumps(mp)) 
        print r.text
        if r.text == 'OK':
            return {'status': 'OK', 'msg': 'success'}
    return {'status': 'Failed', 'reason': r.text}


# if __name__ == '__main__':
