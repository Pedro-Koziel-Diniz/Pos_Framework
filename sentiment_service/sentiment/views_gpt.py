import os
import openai
import joblib
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models_sentiment import PredictionHistory
from .models_cadastro import pessoa

load_dotenv()  
# Configurar a API key da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_sentiment_gpt(content, model="gpt-4o-mini"):
    """
    Usa o modelo OpenAI Chat para classificar o sentimento de um texto.
    Retorna apenas 'pos' ou 'neg'.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Classify the sentiment of the following text as 'pos' for positive or 'neg' for negative."
                        f" Respond with only 'pos' or 'neg' and no additional text.\n\n"
                        f"Text: \"{content}\""
                    ),
                }
            ],
        )
        result = response["choices"][0]["message"]["content"].strip().lower()
        return result if result in ["pos", "neg"] else "invalid"
    except Exception as e:
        print(f"Error processing text: {content}\n{e}")
        return None
    
def sentiment_gpt(request):
    usuario = request.session.get('username', None)

    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('index')

    try:
        usuario_pessoa = pessoa.objects.get(usuario=usuario)
        if not usuario_pessoa.permissao_sentiment_gpt:  # ✅ USANDO O CAMPO CORRETO
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('index')
    except pessoa.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('index')

    return render(request, 'sentiment/sentiment_gpt.html')    

def classify_sentiment_gpt_view(request):
    """
    Chama o modelo GPT para classificar sentimento via API.
    """
    if request.method == 'POST':
        text = request.POST.get('text', '')

        # Corrigindo chamada da função correta
        sentiment = classify_sentiment_gpt(text)  # Correto: Chamando a função de processamento

        if sentiment is None:
            return JsonResponse({'error': 'Erro ao processar sentimento com GPT'}, status=500)

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
            source='sentiment-gpt', 
            user=request.user if request.user.is_authenticated else None, 
            usuario_pessoa=usuario_pessoa
        )

        return JsonResponse({'text': text, 'sentiment': sentiment})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)