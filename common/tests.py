from django.test import TestCase

from mongoengine import connect
from .models import ContestRank, RankUser
# Create your tests here.

class MongoRankTestCase(TestCase):

    def test_add_rankduser_to_contest(self):
        connect('contest')
        c = ContestRank(contest_pk=0)
        c.save()
        u = RankUser(user_pk=1, score=10)
        u.save()
        c.update_one(pull__users=u)
        c.save()
        u2 = RankUser(user_pk=2, score=30)
        u2.save()
        c.update_one(pull__users=u2)
        c.save()
        u3 = RankUser(user_pk=3, score=20)
        u3.save()
        c.update_one(pull__users=u3)
        c.save()
        for x in c.users:
            print x.user_pk




