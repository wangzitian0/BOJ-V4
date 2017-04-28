import django_filters
from django_filters.widgets import BooleanWidget
from .models import Group
from guardian.shortcuts import get_objects_for_user


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    can_manage = django_filters.BooleanFilter(method='filter_can_manage', label='can_manage', widget=BooleanWidget())

    def filter_can_manage(self, queryset, name, value):
        print "<name>:", name
        print "<value>:", value
        profiles_can_change = get_objects_for_user(
                self.user,
                'ojuser.change_groupprofile',
                with_superuser=True
            )
        if value:
            queryset = queryset.filter(pk__in=profiles_can_change)
        else:
            queryset = queryset.exclude(pk__in=profiles_can_change)

        return queryset

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GroupFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Group
        fields = ['name', 'can_manage', ]
