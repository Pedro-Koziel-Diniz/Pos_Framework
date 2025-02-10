from django.db import models

class pessoa(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    usuario = models.CharField(max_length=50, null=False, blank=False, verbose_name='Usuario', default='default_user')
    senha = models.CharField(max_length=50, null=False, blank=False, verbose_name='Senha', default='default_pass')
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name='eMail')
    celular = models.CharField(max_length=20, null=True, blank=True, verbose_name='celular')
    funcao = models.CharField(max_length=30, null=True, blank=True, verbose_name='Funcao')
    nascimento = models.DateField(null=True, blank=True, verbose_name='Nascimento')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    permissao_sentiment_gpt = models.BooleanField(default=False, verbose_name="Acesso Sentiment GPT")
    permissao_sentiment_deepseek = models.BooleanField(default=False, verbose_name="Acesso Sentiment DeepSeek")
    permissao_sentiment_ml = models.BooleanField(default=False, verbose_name="Acesso Sentiment ML")

    def __str__(self):
        return f"{self.nome} - {self.usuario}"

    class Meta:
        ordering = ['nome', 'funcao']

