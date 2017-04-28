import django_filters
from django_filters.widgets import LookupTypeWidget
from .models import Submission
from problem.models import Problem
from guardian.shortcuts import get_objects_for_user

from bojv4.conf import LANGUAGE, STATUS_CODE


class SubmissionFilter(django_filters.FilterSet):

    pk = django_filters.CharFilter(name='id')
    language = django_filters.ChoiceFilter(choices=LANGUAGE.filter_choice())
    problem = django_filters.ModelChoiceFilter(queryset=Problem.objects.all())
    status = django_filters.ChoiceFilter(choices=STATUS_CODE.filter_choice())

    def __init__(self, *args, **kwargs):
        self.problems = kwargs.pop('problems')
        super(SubmissionFilter, self).__init__(*args, **kwargs)
        self.filters.get('problem').queryset=self.problems


    class Meta:
        model = Submission
        fields = ['pk', 'problem', 'language', 'status']

