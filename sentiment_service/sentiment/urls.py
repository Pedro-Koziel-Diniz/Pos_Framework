from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.index, name='index'),
    path('sentiment/', views.sentiment, name='sentiment'),
    path('classify/', views.classify_sentiment, name='classify_sentiment'),
    path('historico/', views.history, name='historico'),
    path('sobre/', views.sobre, name='sobre'),
    path('sentiment-ml/', views.sentiment_ml, name='sentiment_ml'),
    path('predict-sentiment/', views.predict_sentiment, name='predict_sentiment'),
    path('cadastro/', views.cadastro, name='cadastro'),
]