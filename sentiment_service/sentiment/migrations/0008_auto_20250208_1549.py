# Generated by Django 3.2.25 on 2025-02-08 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0007_auto_20250208_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pessoa',
            old_name='permissao_sentiment',
            new_name='permissao_sentiment_gpt',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='permissao_sentiment_deepseek',
            field=models.BooleanField(default=False, verbose_name='Acesso Sentiment DeepSeek'),
        ),
        migrations.AlterField(
            model_name='predictionhistory',
            name='source',
            field=models.CharField(default='sentiment-gpt', max_length=50),
        ),
    ]
