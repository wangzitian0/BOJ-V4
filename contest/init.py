# -*- coding: utf-8 -*-

from User.models import *
from Privilege.models import *
from Problem.models import *
from Contest.models import *
from datetime import datetime

def pre():
    r = Root.objects.create(root_name='hehe', root_name_cn='hehe')
    u = User.addUser('hehehehe', 'hehehehehehehe')
    p = Problem.addProblem(a, 'public', 'hehe', 100, 100, 100, 'hehehehe', 0, 0)
    p = Problem.addProblem(a, 'public', 'hehehe', 100, 100, 100, 'hehehehe', 0, 0)
    p = Problem.addProblem(a, 'public', 'hehehehe', 100, 100, 100, 'hehehehe', 0, 0)
    c = Contest.addContest(u, 'hehe', [(1, '', 'A')], datetime(2014, 4, 2, 1, 1, 1))


def gao():
    for c in Contest.objects.all():
        print c.cid
