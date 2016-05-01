import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import User


class GroupTable(tables.Table):
    name = tables.LinkColumn('mygroup-detail', args=[A('pk')], verbose_name="Group")
    nickname = tables.Column(accessor='profile.nickname', verbose_name="Nickname")
    superadmin = tables.Column(accessor='profile.superadmin', verbose_name="Creater")
    desc = tables.TemplateColumn(
        '{{ record.profile.desc|truncatechars:25 }}',
        verbose_name="Description",
        orderable=False,
    )
    status = tables.TemplateColumn(
        template_name='ojuser/group_list_external.html',
        orderable=False,
    )

    class Meta:
        model = User
        fields = ('name', 'nickname', 'superadmin', 'desc', 'status',)
        template = 'django_tables2/bootstrap.html'


class GroupUserTable(tables.Table):
    status = tables.TemplateColumn('{{ record.email }}')

    class Meta:
        model = User
        fields = ('username', 'email', )
        template = 'django_tables2/bootstrap.html'
