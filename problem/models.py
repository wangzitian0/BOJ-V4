from __future__ import unicode_literals

from django.contrib.auth.models import User
from filer.models.filemodels import File
from django.core.urlresolvers import reverse
from django.db import models
from ojuser.models import GroupProfile
from bojv4.settings import BASE_DIR

#  from filer.fields.file import FilerFileField


class Problem(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    code_length_limit = models.IntegerField(default=65536)
    problem_desc = models.TextField(default='None')
    is_spj = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    superadmin = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    allowed_lang = models.ManyToManyField('ojuser.Language', related_name='problems')
    groups = models.ManyToManyField(GroupProfile, blank=True, related_name='problems')

    def __unicode__(self):
        return str(self.pk) + " " + str(self.title)

    def get_absolute_url(self):
        return reverse('problem:problem-detail', kwargs={'pk': self.pk})


    def view_by_user(self, user):
        for g in self.groups.all():
            if user.has_perm('ojuser.view_groupprofile', g):
                return True
        return False


    def check_data(self):
        data_info = self.datainfo
        in_set = set()
        out_set = set()
        mp = {}
        for f in data_info.all():
            data = f.data
            path = data.path
            filename = path[path.rfind('/') + 1:]
            mp[filename] = data
            if path.endswith('.in'):
                if filename in in_set:
                    return False
                in_set.add(filename)
            elif path.endswith('.out'):
                if filename in out_set:
                    return False
                out_set.add(filename)
        if len(in_set) !=  len(out_set):
            return False
        cases = []
        for x in in_set:
            case = ProblemCase()
            case.problem = self
            case.input_data = mp[x]
            outfile = x.rstrip('.in') + '.out'
            if outfile in out_set:
                case.output_data = mp[outfile]
            else:
                return False
            cases.append(case)

        for cas in cases:
            cas.save()
            print 'pk: ', cas.pk
            print 'input: ', cas.input_data.path
            print 'output: ', cas.output_data.path
        return True


    def get_problem_data(self):
        resp = []
        p_count = 0
        for cas in self.case.all():
            in_data = {
                    'filename': cas.input_data.sha1,
                    'path': '/' + cas.input_data.path.lstrip(BASE_DIR)
                    }
            out_data = {
                    'filename': cas.output_data.sha1,
                    'path': '/' + cas.output_data.path.lstrip(BASE_DIR)
                    }
            resp.append({
                'in': in_data,
                'out': out_data,
                'position': p_count
                })
            p_count += 0
            print in_data['path']
        return resp


    class Meta:
        permissions = (
            ('view_problem', 'Can view problem'),
        )


def upload_dir(instance, filename):
    return 'documents/{0}/{1}'.format(instance.problem.pk, str(filename))


class ProblemDataInfo(models.Model):
    problem = models.ForeignKey(Problem, related_name="datainfo")
    data = models.OneToOneField(File, null=True, blank=True, related_name="datainfo")

    def __unicode__(self):
        return str(self.problem.pk) + " " + str(self.pk)

class ProblemCase(models.Model):
    problem = models.ForeignKey(Problem, related_name="case")
    input_data = models.OneToOneField(File, null=True, blank=True, related_name="incase")
    output_data = models.OneToOneField(File, null=True, blank=True, related_name="outcase")
    score = models.IntegerField(default=0)
    info = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.problem.pk) + ":" + str(self.pk)

    @property
    def get_input_name(self):
        path = self.input_data.path
        return path[path.rfind('/') + 1:]

    @property
    def get_output_name(self):
        path = self.output_data.path
        return path[path.rfind('/') + 1:]



