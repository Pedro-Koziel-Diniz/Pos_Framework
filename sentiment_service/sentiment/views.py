import os
import openai
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

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
        if result in ["pos", "neg"]:
            return result
        else:
            return "invalid"
    except Exception as e:
        print(f"Error processing text: {content}\n{e}")
        return None

def index(request):
    return render(request, 'sentiment/index.html')

def classify_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        sentiment = classify_sentiment_gpt(text)
         # Se o sentimento for "neg", converte para "NEGATIVO"
        if sentiment == "neg":
            sentiment = "NEGATIVO"
        # Se o sentimento for "pos", converte para "POSITIVO"
        elif sentiment == "pos":
            sentiment = "POSITIVO"
        return JsonResponse({'text': text, 'sentiment': sentiment})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
