import os
import openai
import joblib
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .models import PredictionHistory

load_dotenv()  # take environment variables from .env.

# Configurar a API key da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def index(request):    
    usuario = request.POST.get('username')
    senha = request.POST.get('password')
    user = authenticate(username=usuario, password=senha)
    if (user is not None):
        login(request, user)
        request.session['username'] = usuario
        request.session['password'] = senha
        request.session['usernamefull'] = user.get_full_name()
        print(request.session['username'])
        print(request.session['password'])
        print(request.session['usernamefull'])
        return redirect('sentiment/')
    else:
        data = {}
        if (usuario):
            data['msg'] = "Usuário ou Senha Incorretos "
        return render(request, 'sentiment/login.html', data)

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

def sentiment(request):
    return render(request, 'sentiment/sentiment.html')

def sobre(request):
    return render(request, 'sentiment/sobre.html')

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
        PredictionHistory.objects.create(text=text, sentiment=sentiment)
        return JsonResponse({'text': text, 'sentiment': sentiment})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

### Modelos de classificação por ML
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(PROJECT_DIR, 'machine_learning', 'models')

# Caminhos absolutos para os modelos
CLASSIFIER_PATH = os.path.join(MODEL_DIR, 'sentiment_classifier_model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')

classifier = joblib.load(CLASSIFIER_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def sentiment_ml(request):
    # Renderiza o formulário HTML
    return render(request, 'sentiment/sentiment_ml.html')

def predict_sentiment(request):
    # Captura o texto enviado via GET
    new_text = request.GET.get('text', '')
    if not new_text:
        return JsonResponse({'error': 'Texto não fornecido'}, status=400)

    try:
        # Converte o texto para o formato necessário pelo vetor TF-IDF
        new_text_tfidf = vectorizer.transform([new_text])
        # Realiza a previsão com o modelo
        predicted_label_encoded = classifier.predict(new_text_tfidf)
        # Tenta converter a previsão de volta para o rótulo original
        try:
            predicted_label = label_encoder.inverse_transform(predicted_label_encoded)
        except ValueError as e:
            # Em caso de erro, significa que o modelo está tentando usar um rótulo desconhecido
            return JsonResponse({'error': f'Rótulo desconhecido detectado: {str(e)}'}, status=400)
        PredictionHistory.objects.create(text=new_text, sentiment=predicted_label[0])
        # Retorna o resultado como JSON
        return JsonResponse({
            'texto': new_text,
            'sentimento_previsto': predicted_label[0]})
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro detalhada
        return JsonResponse({'error': f'Erro ao processar o texto: {str(e)}'}, status=500)

def history(request):
    predictions = PredictionHistory.objects.all().order_by('-created_at')  # Recupera o histórico
    return render(request, 'sentiment/historico.html', {'predictions': predictions})