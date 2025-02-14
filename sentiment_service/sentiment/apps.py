from django.apps import AppConfig

class SentimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sentiment'
    verbose_name = "Análise de Sentimento"  # Nome legível para o admin
