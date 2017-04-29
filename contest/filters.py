import django_filters
from django_filters.widgets import BooleanWidget
from django_filters import widgets
from django_filters import filters
from .models import Contest, ContestSubmission
from ojuser.models import GroupProfile
from guardian.shortcuts import get_objects_for_user

from bojv4.conf import LANGUAGE, STATUS_CODE
#  from guardian.shortcuts import get_objects_for_user


class SubmissionFilter(django_filters.FilterSet):

    pk = django_filters.CharFilter(name='id', label='id')
    submission__language = django_filters.ChoiceFilter(choices=LANGUAGE.choice(), label='language')
    problem = django_filters.ModelChoiceFilter(queryset=(('A', 'A'),))
    submission__status = django_filters.ChoiceFilter(choices=STATUS_CODE.choice(), label='status')

    def __init__(self, *args, **kwargs):
        self.problems = kwargs.pop('problems')
        super(SubmissionFilter, self).__init__(*args, **kwargs)
        self.filters.get('problem').queryset=self.problems


    class Meta:
        model = ContestSubmission
        fields = ['pk', 'problem', 'submission__language', 'submission__status']
        order_by = 'desc'


def view_groups(request):
    print 'user name', request.user
    queryset = get_objects_for_user(
                    request.user,
                    'ojuser.view_groupprofile',
                    with_superuser=True
                ).distinct().all()
    return queryset


class ContestFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='name')
    group = django_filters.ModelChoiceFilter(queryset=GroupProfile.objects.all())
    can_manage = django_filters.BooleanFilter(method='filter_can_manage', label='can_manage')

    def filter_can_manage(self, queryset, value):
        groups = get_objects_for_user(
            self.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        ).distinct()
        if value:
            return queryset.filter(pk__in=groups)
        else:
            return queryset.exclude(pk__in=groups)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContestFilter, self).__init__(*args, **kwargs)
        self.filters.get('group').queryset = get_objects_for_user(self.user, 'ojuser.view_groupprofile', with_superuser=True)


    class Meta:
        model = Contest
        fields = ['name', 'group', 'can_manage', ]


