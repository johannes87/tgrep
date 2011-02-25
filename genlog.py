#!/usr/bin/python

from time import strftime, gmtime
import random

template='127.0.0.1 - frank [%d/%b/%Y:%H:%M:%S -0700] "GET {0} /apache_pb.gif HTTP/1.0" 200 2326'

t_secs = 0
while True:
    print strftime(template, gmtime(t_secs)).format(random.randint(0,30) * ' ')
    t_secs += 10
