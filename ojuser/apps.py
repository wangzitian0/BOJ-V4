from __future__ import unicode_literals

from django.apps import AppConfig


class OjuserConfig(AppConfig):
    name = 'ojuser'
    verbose_name = 'Oj User Application'

    def ready(self):
        from . import signals
