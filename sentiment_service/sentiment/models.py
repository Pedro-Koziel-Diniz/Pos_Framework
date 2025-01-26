from django.db import models

# Create your models here.
class pessoa(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name='eMail')
    celular = models.CharField(max_length=20, null=True, blank=True, verbose_name='celular')
    funcao = models.CharField(max_length=30, null=True, blank=True, verbose_name='Funcao')
    nascimento = models.DateField(null=True, blank=True, verbose_name='Nascimento')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['nome', 'funcao',]

class PredictionHistory(models.Model):
    text = models.TextField()  # Texto inserido
    sentiment = models.CharField(max_length=50)  # Sentimento previsto
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora da previsão

    def __str__(self):
        return f"{self.text[:50]}... - {self.sentiment}"
