import django_filters
from django_filters.widgets import BooleanWidget
from .models import Problem
#  from guardian.shortcuts import get_objects_for_user


class ProblemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    can_manage = django_filters.MethodFilter(widget=BooleanWidget())

    def filter_can_manage(self, queryset, value):
        return queryset

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProblemFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Problem
        fields = ['title', 'can_manage', ]
