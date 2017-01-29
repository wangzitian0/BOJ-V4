
import requests


def send_to_nsq(topic, message):
    if not isinstance(message, str):
        return {'code': -1, 'reason': 'the message must be string'}
    if not isinstance(topic, str):
        return {'code': -1, 'reason': 'the topic must be string'}
    url = "http://127.0.0.1:4151/put?topic=" + topic
    r = requests.post(url, data=message) 
    print r.text
    if r.text == 'OK':
        return {'code': 0, 'msg': 'success'}
    else:
        return {'code': -1, 'reason': r.text}

if __name__ == '__main__':
    send_to_nsq('test_topic', 'xixihaha')
    send_to_nsq('test_topic', 'haha')
    send_to_nsq('test_topic', 'xixi')

