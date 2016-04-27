import django_filters
from .models import Group


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Group
        fields = ['name', ]
