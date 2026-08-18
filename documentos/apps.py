from django.apps import AppConfig


class DocumentosConfig(AppConfig):
    name = 'documentos'

    def ready(self):
      import documentos.signals 
