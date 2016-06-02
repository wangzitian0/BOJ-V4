import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import User
from .models import GroupProfile


class GroupTable(tables.Table):
    name = tables.LinkColumn('mygroup-detail', args=[A('pk')], verbose_name="Group")
    nickname = tables.Column(accessor='nickname', verbose_name="Nickname")
    superadmin = tables.Column(accessor='superadmin', verbose_name="Creater")
    desc = tables.TemplateColumn(
        '{{ record.desc|truncatechars:25 }}',
        verbose_name="Description",
        orderable=False,
    )
    status = tables.TemplateColumn(
        template_name='ojuser/group_list_external.html',
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = GroupProfile
        order_by = ['name']
        fields = ('name', 'nickname', 'superadmin', 'desc', 'status',)
        template = 'django_tables2/bootstrap.html'


class GroupUserTable(tables.Table):
    status = tables.TemplateColumn('{{ record.email }}')

    class Meta:
        model = User
        fields = ('username', 'email', )
        template = 'django_tables2/bootstrap.html'
