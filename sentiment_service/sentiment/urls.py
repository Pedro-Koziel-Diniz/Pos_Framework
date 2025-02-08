from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.index, name='index'),  
    path('sentiment-gpt/', views.sentiment_gpt, name='sentiment_gpt'),
    path('sentiment-deepseek/', views.sentiment_deepseek, name='sentiment_deepseek'),
    path('classify-gpt/', views.classify_sentiment_gpt_view, name='classify_sentiment_gpt'),
    path('classify-deepseek/', views.classify_sentiment_deepseek_view, name='classify_sentiment_deepseek'),
    path('historico/', views.history, name='historico'),
    path('sobre/', views.sobre, name='sobre'),
    path('sentiment-ml/', views.sentiment_ml, name='sentiment_ml'),
    path('predict-sentiment/', views.predict_sentiment, name='predict_sentiment'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
