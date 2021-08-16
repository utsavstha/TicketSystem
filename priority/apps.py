from django.apps import AppConfig


class PriorityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'priority'
    def ready(self):
        import priority.signals