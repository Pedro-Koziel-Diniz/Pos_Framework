import os
import requests
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models_sentiment import PredictionHistory
from .models_cadastro import pessoa

load_dotenv() 
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

def classify_sentiment_deepseek(content, model="deepseek-chat"):
    """
    Usa a API da DeepSeek para classificar o sentimento de um texto.
    Retorna apenas 'pos' ou 'neg'.
    """
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Classify the sentiment of the following text as 'pos' for positive or 'neg' for negative."
                        " Respond with only 'pos' or 'neg' and no additional text.\n\n"
                        f"Text: \"{content}\""
                    ),
                }
            ],
            "temperature": 0.2,
            "max_tokens": 10
        }
        
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()

        # **Verifica se a resposta contém erro**
        if "error" in response_data:
            error_code = response_data["error"].get("code")
            error_message = response_data["error"].get("message", "Erro desconhecido na API DeepSeek")
            
            if error_code == "invalid_request_error":
                print(f"⚠️ DeepSeek API Error: {response_data}")
                return "Insufficient Balance"  # Retorna um aviso claro
            
            print(f"DeepSeek API Error: {response_data}")
            return None  # Retorna erro genérico

        if "choices" in response_data:
            result = response_data["choices"][0]["message"]["content"].strip().lower()
            return result if result in ["pos", "neg"] else "invalid"

        return None

    except Exception as e:
        print(f"Error processing text: {content}\n{e}")
        return None

def sentiment_deepseek(request):
    """
    Página da análise de sentimento usando DeepSeek.
    """
    usuario = request.session.get('username', None)

    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('index')

    try:
        usuario_pessoa = pessoa.objects.get(usuario=usuario)
        if not usuario_pessoa.permissao_sentiment_deepseek:
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('index')
    except pessoa.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('index')

    return render(request, 'sentiment/sentiment_deepseek.html')    

def classify_sentiment_deepseek_view(request):
    """
    Chama o modelo DeepSeek para classificar sentimento via API.
    """
    if request.method == 'POST':
        text = request.POST.get('text', '')

        sentiment = classify_sentiment_deepseek(text)
        
        if sentiment == "Insufficient Balance":
            return JsonResponse({'error': 'Saldo insuficiente para consulta na API DeepSeek.'}, status=402)

        if sentiment is None:
            return JsonResponse({'error': 'Erro ao processar sentimento com DeepSeek'}, status=500)

        sentiment = "NEGATIVO" if sentiment == "neg" else "POSITIVO" if sentiment == "pos" else "INVÁLIDO"

        # Verifica usuário autenticado
        usuario_pessoa = None
        if 'username' in request.session and not request.user.is_authenticated:
            try:
                usuario_pessoa = pessoa.objects.get(usuario=request.session['username'])
            except pessoa.DoesNotExist:
                usuario_pessoa = None

        # Salva no histórico
        PredictionHistory.objects.create(
            text=text, 
            sentiment=sentiment, 
            source='sentiment-deepseek', 
            user=request.user if request.user.is_authenticated else None, 
            usuario_pessoa=usuario_pessoa
        )

        return JsonResponse({'text': text, 'sentiment': sentiment})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
