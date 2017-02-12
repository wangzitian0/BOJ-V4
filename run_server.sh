#!/bin/bash

python ./consume.py >> consume.log & echo $! > temp1.pid
redis-server >> redis.log & echo $! > temp2.pid
nsqd --lookupd-tcp-address=127.0.0.1:4160 >> nsqd.log & echo $! > temp3.pid
nsqadmin --lookupd-http-address=127.0.0.1:4161 >> nsqadmin.log & echo $! > temp4.pid
nsqlookupd >> nsqlookupd.log & echo $! > temp5.pid


