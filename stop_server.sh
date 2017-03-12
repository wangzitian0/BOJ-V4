#!/bin/bash
cat ./temp1.pid | xargs -IX kill -9 X
cat ./temp2.pid | xargs -IX kill -9 X
cat ./temp3.pid | xargs -IX kill -9 X
cat ./temp4.pid | xargs -IX kill -9 X
cat ./temp5.pid | xargs -IX kill -9 X
rm *.pid
rm *.dat
rm *.log

