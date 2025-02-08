from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class pessoa(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    usuario = models.CharField(max_length=50, null=False, blank=False, verbose_name='Usuario', default='default_user')
    senha = models.CharField(max_length=50, null=False, blank=False, verbose_name='Senha', default='default_pass')
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name='eMail')
    celular = models.CharField(max_length=20, null=True, blank=True, verbose_name='celular')
    funcao = models.CharField(max_length=30, null=True, blank=True, verbose_name='Funcao')
    nascimento = models.DateField(null=True, blank=True, verbose_name='Nascimento')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.sentiment}"
        elif self.usuario_pessoa:
            return f"{self.usuario_pessoa.usuario} - {self.sentiment}"
        return f"Anônimo - {self.sentiment}"
    class Meta:
        ordering = ['nome', 'funcao',]

class PredictionHistory(models.Model):
    text = models.TextField()  # Texto inserido
    sentiment = models.CharField(max_length=50)  # Sentimento previsto
    source = models.CharField(max_length=50, default="sentiment")  # Origem do registro
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora da previsão
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    usuario_pessoa = models.ForeignKey('pessoa', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.text[:50]}... - {self.sentiment}"
