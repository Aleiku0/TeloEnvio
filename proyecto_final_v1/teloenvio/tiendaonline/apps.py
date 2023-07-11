from django.apps import AppConfig


class TiendaonlineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tiendaonline'
    
    def ready(self):
            import tiendaonline.signals  # Importar el archivo signals.py