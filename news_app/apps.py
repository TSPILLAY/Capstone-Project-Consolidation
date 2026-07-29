from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    """Application configuration for news_app."""
    
    name = 'news_app'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """
        Import signals module upon application initialization to register signal receivers.
        """
        import news_app.signals
