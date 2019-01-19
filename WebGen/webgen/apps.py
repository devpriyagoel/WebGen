from django.apps import AppConfig


class WebgenConfig(AppConfig):
    name = 'webgen'

    def ready(self):
    	import webgen.signals