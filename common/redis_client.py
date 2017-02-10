
import redis
from submission.models import Submission
from contest.serializers import UserSerializer
from datetime import datetime, timedelta


pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)

def calc_contest_score(sub):
    if not sub.contest:
        return
    z_key = str(sub.contest.pk) + sub.contest.name
    s_key = str(sub.user.pk) + sub.user.username
    u_key = str(sub.contest.pk) + '--' + str(sub.user.pk)
    if not r.get(u_key):
        us = UserSerializer(user_pk=sub.user.pk, user_name=sub.user.user_name,
                contest_pk=sub.contest.pk, cost_time=0, all_sub=0, 
                problem_ac={}, problem_time={}, problem_sub={}) 
    else:
        us = UserSerializer(data=r.get(u_key))
    if not r.zscore(z_key, s_key):
        r.zadd(z_key, s_key=0)
    dura = datetime.now() - sub.contest.start_time
    us.all_sub += 1
    pkey = str(sub.problem.pk)
    us.problem_sub[pkey] += 1
    if Submission.firstAcInContest(sub):
        r.incrby(z_key, s_key, 10000) 
        us.problem_ac[pkey] += 1
        us.cost_time += us.problem_time[pkey] + dura 
    elif Submission.notAcInContest(sub):
        r.incrby(z_key, s_key, -1)
        us.problem_time[pkey] += timedelta(minute=20)
    r.setex(u_key, 18000, us.toJson())

def get_contest_rank_info(contest):
    z_key = str(contest.pk) + contest.name
    return r.zrange(z_key, -1, -1, desc=True, withscore=True) 


