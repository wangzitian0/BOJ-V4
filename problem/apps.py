from __future__ import unicode_literals

from django.apps import AppConfig


class ProblemConfig(AppConfig):
    name = 'problem'

    def ready(self):
        from . import signals
