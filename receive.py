import nsq

def handler(message):
    print 'consume2==========='
    print message.body
    return True

r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=['127.0.0.1:4150'],
        topic='submission', channel='asdfxx', lookupd_poll_interval=15)

nsq.run()
