from django.db import models
from django.contrib.auth.models import User
from .models_cadastro import pessoa

class PredictionHistory(models.Model):
    text = models.TextField()  
    sentiment = models.CharField(max_length=50)  
    source = models.CharField(max_length=50, default="sentiment_gpt")  
    created_at = models.DateTimeField(auto_now_add=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    usuario_pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.text[:50]}... - {self.sentiment}"
