# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Contest, ContestProblem, ContestNotification, ContestProblemSubmission, Clarification
from datetime import datetime, timedelta
from ojuser.models import GroupProfile
import logging
# Create your views here.
contest = Contest()
contest.start_time = datetime(2014, 7, 20, 13, 0, 0)
contest.cid = 1
contest.title = "2014新生暑假个人排位赛1"
contest.description = "2014年新生暑假训练第一场排位赛"
contest.contest_type = 0
contest.group = "ACM-ICPC"
    #grp = GroupProfile()
    #grp.name="2014-test_courese"
    #grp.nickname="ACM-ICPC"
cp_list = list()
cp=ContestProblem()
cp.cp_index="A"
cp.cp_score=100
cp.cp_title="学姐的桌面"
cp.p_id=1
cp.tlimt=1000
cp.mlimt=65536
cp.ac = 37
cp.sub = 63
cp.ratio = cp.ac*100.0/cp.sub
cp_list.append(cp)
cp=ContestProblem()
cp.cp_index="B"
cp.cp_score=100
cp.cp_title="学姐去学车"
cp.p_id=2
cp.tlimt=1000
cp.mlimt=65536
cp.ac = 31
cp.sub = 119
cp.ratio = cp.ac*100.0/cp.sub
cp_list.append(cp)
cp=ContestProblem()
cp.cp_index="C"
cp.cp_score=100
cp.cp_title="学姐的学弟"
cp.p_id=3
cp.tlimt=1000
cp.mlimt=65536
cp.ac = 3
cp.sub = 14
cp.ratio = cp.ac*100.0/cp.sub
cp_list.append(cp)
cp=ContestProblem()
cp.cp_index="D"
cp.cp_score=100
cp.cp_title="BLOCKS"
cp.p_id=4
cp.tlimt=1000
cp.mlimt=65536
cp.ac = 10
cp.sub = 84
cp.ratio = cp.ac*100.0/cp.sub
cp_list.append(cp)
cp=ContestProblem()
cp.cp_index="E"
cp.cp_score=100
cp.cp_title="数的关系"
cp.p_id=5
cp.tlimt=1000
cp.mlimt=65536
cp.ac = 7
cp.sub = 66
cp.ratio = cp.ac*100.0/cp.sub
cp_list.append(cp)


def testProblem(request):
    return render(request, 'contest/test/testproblem.html')

def listContestByUser(request, pageId='1'):
    """
    view used to list all contest a user can participate
    """
    c = contest
    c.status="ended"
    contest_list = list()
    contest_list.append(c)
    return render(request, 'contest/contestList.html', {"contest_list":contest_list})

def showContest(request, cid):

    c = contest
    c.status = "ended"
    c.time_left = 0
    c.time_passed_percent = 100
    cn_list = list()
    cn = ContestNotification()
    cn.time = c.start_time+timedelta(minutes=30)
    cn.title = "A题"
    cn.content = "A题就不要做了"
    cn.cnid = 1
    cn_list.append(cn)

    res = {'contest': c, 'problem_list': cp_list, 'contest_notice_list':cn_list, 'tpl':{'has_priv': True, 'nav_act':'contest',}}

    return render(request, 'contest/showContest.html', res)

def showContestProblem(request, cid, cpidx):
    c = contest
    c.status = "ended"
    c.time_left = 0
    c.time_passed_percent = 100
    cn_list = list()
    cn = ContestNotification()
    cn.time = c.start_time+timedelta(minutes=30)
    cn.title = "A题"
    cn.content = "A题就不要做了"
    cn.cnid = 1
    cn_list.append(cn)
    res = {'contest': c,
           'problem_list': cp_list,
           'contest_notice_list':cn_list,
           'contest_problem':cp,
           'tpl':{'has_priv': True, 'nav_act':'contest',},}

    return render(request, 'contest/showProblem.html', res)

def showStatus(request, cid):
    """
    @view: list submission of some contest
    """
    c = contest
    c.status = "ended"
    c.time_left = 0
    c.time_passed_percent = 100
    cps_list = list()
    cps = ContestProblemSubmission()
    cps.cpsid = 1
    cps.cps_results = 1023
    cps.cp_index = 'A'
    cps.cps_codelength = 789
    cps.cps_timecost = 876
    cps.cps_memerycost = 37
    cps.cps_status = "通过"
    cps.cps_status_class = "status-ac"
    cps.cps_language = 0
    cps.cps_score = 100
    cps.cps_submittime = datetime(2014, 7, 20, 13, 30, 28)
    cps.cps_username = "hnnwang"
    cps_list.append(cps)

    cps = ContestProblemSubmission()
    cps.cpsid = 0
    cps.cps_results = 1022
    cps.cp_index = 'A'
    cps.cps_codelength = 774
    cps.cps_timecost = 864
    cps.cps_memerycost = 35
    cps.cps_status = "答案错误"
    cps.cps_status_class = "status-wa"
    cps.cps_score = 90
    cps.cps_language = 0
    cps.cps_username = "hnnwang"
    cps.cps_submittime = datetime(2014, 7, 20, 13, 20, 54)
    cps_list.append(cps)
    res = {'contest': c,
           'problem_list': cp_list,
           'submission_list':cps_list,
           'contest_problem':cp,
           'tpl':{'has_priv': True, 'nav_act':'contest',},}
    return render(request, 'contest/showStatus.html', res)


def showBoard(request, cid):
    c = contest

    c.status = "ended"
    c.time_left = 0
    c.time_passed_percent = 100
    cn_list = list()
    cn = ContestNotification()
    cn.time = c.start_time+timedelta(minutes=30)
    cn.title = "A题"
    cn.content = "A题就不要做了"
    cn.cnid = 1
    cn_list.append(cn)
    board_list = list()
    single_item = dict()
    single_item = {
        "rank":1,
        "username":"vegetable_chicken",
        "solve":5,
        "score":500,
        "penalty":622,
        "info":[{"sub_times":1, "ac_time":11, "score":100},
        {"sub_times":3, "ac_time":80, "score":100},
        {"sub_times":4, "ac_time":50, "score":100, "fb":True},
        {"sub_times":4, "ac_time":225, "score":100},
        {"sub_times":1, "ac_time":96, "score":100}]
    }
    board_list.append(single_item)
    single_item = dict()
    single_item = {
        "rank":2,
        "username":"skyxuan",
        "solve":4,
        "score":400,
        "penalty":522,
        "info":[{"sub_times":1, "ac_time":14, "score":100},
        {"sub_times":2, "ac_time":43, "score":100},
        {"sub_times":0, "ac_time":-1, "score":0},
        {"sub_times":6, "ac_time":121, "score":100, "fb":True},
        {"sub_times":4, "ac_time":164, "score":100}]
    }
    board_list.append(single_item)
    single_item = dict()
    single_item = {
        "rank":3,
        "username":"ggvalid",
        "solve":4,
        "score":400,
        "penalty":525,
        "info":[{"sub_times":1, "ac_time":27, "score":100},
        {"sub_times":3, "ac_time":113, "score":100},
        {"sub_times":0, "ac_time":-1, "score":0},
        {"sub_times":6, "ac_time":172, "score":100},
        {"sub_times":1, "ac_time":73, "score":100, "fb":True}]
    }
    board_list.append(single_item)
    single_item = dict()
    single_item = {
        "rank":4,
        "username":"xixihaha",
        "solve":3,
        "score":300,
        "penalty":312,
        "info":[{"sub_times":1, "ac_time":6, "score":100, "fb":True},
        {"sub_times":2, "ac_time":36, "score":100},
        {"sub_times":0, "ac_time":-1, "score":0},
        {"sub_times":4, "ac_time":190, "score":100},
        {"sub_times":2, "ac_time":-1, "score":30}]
    }
    board_list.append(single_item)
    res = {'contest': c,
           'problem_list': cp_list,
           'board_list':board_list,
           'tpl':{'has_priv': True, 'nav_act':'contest',},}

    return render(request, 'contest/showBoard.html', res)

def showQuery(request, cid):
    c = contest
    cp_list = list()
    cp=ContestProblem()
    cp.cp_index="A"
    cp.cp_score=100
    cp.cp_title="题目A"
    cp.p_id=1
    cp.tlimt=1000
    cp.mlimt=65536
    cp.ac = 10
    cp.sub = 20
    cp.ratio = cp.ac*100.0/cp.sub
    cp_list.append(cp)
    c.status = "ended"
    c.time_left = 0
    c.time_passed_percent = 100

    qry_list = list()
    qry = Clarification()
    qry.cp_index="A"
    qry.username = "imzhazha"
    qry.question = "A 第一题为什么是80%。。。学姐的开机速度不是最慢的么。。。"
    qry.answer = "请仔细读题"
    qry_list.append(qry)
    qry = Clarification()
    qry.username = "233"
    qry.cp_index="A"
    qry.question = "还是跪QAQ"
    qry_list.append(qry)
    res = {'contest': c,
           'problem_list': cp_list,
           'query_list': qry_list,
           'tpl':{'has_priv': True, 'nav_act':'contest',},}

    return render(request, 'contest/showQuery.html', res)