from django.test import TestCase
from ojuser.models import Language
from .models import Submission
from django.contrib.auth.models import User, Group

# Create your tests here.

class AddSubmissionTest(TestCase):

    def test_add_submission():
        l = Language.objects.first()
        if not l:
            l = Language.objects.create(key='g++_key', name='g++')
            l.save()
        s = Submission.objects.create() 
