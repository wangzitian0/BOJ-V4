import django_filters
from .models import Group
from guardian.shortcuts import get_objects_for_user


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    can_manage = django_filters.BooleanFilter(action='filter_can_manage')

    def filter_can_manage(self, queryset, value):
        return queryset
        if value:
            return get_objects_for_user(self.request.user, 'change_groupprofile')
        return queryset

    class Meta:
        model = Group
        fields = ['name', ]
