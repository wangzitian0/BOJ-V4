import django_tables2 as tables
from django.contrib.auth.models import User


class GroupUserTable(tables.Table):
    class Meta:
        model = User
        fields = ('username', 'email', )
        template = 'django_tables2/bootstrap.html'
