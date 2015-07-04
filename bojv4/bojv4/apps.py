from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "bojv4"

    def ready(self):
        import_module("bojv4.receivers")
