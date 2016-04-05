from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem, Language
from django.core.urlresolvers import reverse


class Submission(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    datetime = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE")
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(blank=True)
    code = models.TextField()
    Language = models.ForeignKey(Language, related_name='submissions')

    def __unicode__(self):
        return "-".join([str(self.pk), str(self.user), str(self.problem), str(self.datetime)])

    def get_absolute_url(self):
        return reverse('submission:submission-detail', kwargs={'pk': self.pk})
