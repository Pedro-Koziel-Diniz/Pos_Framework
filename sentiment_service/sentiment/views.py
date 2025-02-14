import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models_sentiment import PredictionHistory
from .models_cadastro import pessoa

def index(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        # Primeiro, tenta autenticar com o sistema padrão do Django
        user = authenticate(username=usuario, password=senha)
        if user is not None:
            login(request, user)
            request.session['username'] = usuario
            request.session['password'] = senha
            request.session['usernamefull'] = user.get_full_name()
            return redirect('sentiment_gpt')  # Usuário Django sempre vai para sentiment

        # Se falhar, tenta autenticar no modelo `pessoa`
        try:
            usuario_pessoa = pessoa.objects.get(usuario=usuario, senha=senha)
            if usuario_pessoa.ativo:  # Verifica se o usuário está ativo
                request.session['username'] = usuario_pessoa.usuario
                request.session['usernamefull'] = usuario_pessoa.nome
                
                # **Lógica de Redirecionamento Baseada nas Permissões**
                if usuario_pessoa.permissao_sentiment_gpt:
                    return redirect('sentiment_gpt')  # GPT
                elif usuario_pessoa.permissao_sentiment_deepseek:
                    return redirect('sentiment_deepseek')  # DeepSeek
                elif usuario_pessoa.permissao_sentiment_ml:
                    return redirect('sentiment_ml')  # Machine Learning
                else:
                    messages.error(request, "Você não tem permissão para acessar o sistema.")
                    return redirect('index')

            else:
                messages.error(request, "Usuário inativo. Contate o administrador.")

        except pessoa.DoesNotExist:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'sentiment/login.html')

def sobre(request):
    return render(request, 'sentiment/sobre.html')

def history(request):
    predictions = PredictionHistory.objects.all().order_by('-created_at')  # Recupera o histórico
    return render(request, 'sentiment/historico.html', {'predictions': predictions})