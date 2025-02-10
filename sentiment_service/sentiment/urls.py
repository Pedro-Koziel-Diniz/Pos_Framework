from django.urls import path
from .views import index, sobre, history
from .views_cadastro import cadastro
from .views_gpt import sentiment_gpt, classify_sentiment_gpt_view
from .views_deepseek import sentiment_deepseek, classify_sentiment_deepseek_view
from .views_ml import sentiment_ml, predict_sentiment
from .views_token import CustomAuthToken  # Import para autenticação personalizada

urlpatterns = [
    path('', index, name='index'),
    path('login/', index, name='login'), 
    path('cadastro/', cadastro, name='cadastro'),
    
    # Sentiment Analysis Views
    path('sentiment-gpt/', sentiment_gpt, name='sentiment_gpt'),
    path('sentiment-deepseek/', sentiment_deepseek, name='sentiment_deepseek'),
    path('sentiment-ml/', sentiment_ml, name='sentiment_ml'),

    # Classificação de Sentimento
    path('classify-gpt/', classify_sentiment_gpt_view, name='classify_sentiment_gpt'),
    path('classify-deepseek/', classify_sentiment_deepseek_view, name='classify_sentiment_deepseek'),
    path('predict-sentiment/', predict_sentiment, name='predict_sentiment'),

    # Páginas gerais
    path('historico/', history, name='historico'),
    path('sobre/', sobre, name='sobre'),

    # API Token Authentication
    path('api/token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]
