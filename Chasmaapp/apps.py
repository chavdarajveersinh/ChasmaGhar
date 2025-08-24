from django.apps import AppConfig

class ChasmaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chasmaapp'

    def ready(self):
        from .models import insert_default_products
        insert_default_products()
