import os
import multiprocessing
# before your oj-server starts, execute this python file and the nsq will work.

def workCommand(c):
    print "execute command: ", c
    os.system(c)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=workCommand, args = ('nsqlookupd',))
    p2 = multiprocessing.Process(target=workCommand, 
            args = ('nsqd --lookupd-tcp-address=127.0.0.1:4160',))
    p3 = multiprocessing.Process(target=workCommand, 
            args = ('nsqadmin --lookupd-http-address=127.0.0.1:4161',))

    p1.start()
    p2.start()
    p3.start()


