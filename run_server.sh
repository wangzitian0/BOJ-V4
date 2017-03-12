#!/bin/bash

# python ./consume.py >> consume.log & echo $! > temp1.pid
nohup redis-server >> redis.log & echo $! > temp2.pid
nohup nsqd --lookupd-tcp-address=127.0.0.1:4160 >> nsqd.log & echo $! > temp3.pid
nohup nsqadmin --lookupd-http-address=127.0.0.1:4161 >> nsqadmin.log & echo $! > temp4.pid
nohup nsqlookupd >> nsqlookupd.log & echo $! > temp5.pid


