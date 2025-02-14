import os
import joblib
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.http import JsonResponse  
from django.contrib import messages
from .models_sentiment import PredictionHistory
from .models_cadastro import pessoa

load_dotenv()

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(PROJECT_DIR, "machine_learning", "models")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def sentiment_ml(request):
    usuario = request.session.get("username", None)
    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("index")

    try:
        usuario_pessoa = pessoa.objects.get(usuario=usuario)
        if not usuario_pessoa.permissao_sentiment_ml:
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect("index")
    except pessoa.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("index")

    return render(request, "sentiment/sentiment_ml.html")

def predict_sentiment(request):
    new_text = request.GET.get("text", "").strip()
    selected_models = request.GET.get("models", "LogisticRegression").split(",")

    if not new_text:
        return JsonResponse({"error": "Texto não fornecido"}, status=400)

    results = {}
    try:
        new_text_tfidf = vectorizer.transform([new_text])

        usuario_pessoa = None
        if "username" in request.session and not request.user.is_authenticated:
            try:
                usuario_pessoa = pessoa.objects.get(usuario=request.session["username"])
            except pessoa.DoesNotExist:
                usuario_pessoa = None

        for model_name in selected_models:
            model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")
            if os.path.exists(model_path):
                classifier = joblib.load(model_path)
                predicted_label_encoded = classifier.predict(new_text_tfidf)
                predicted_label = label_encoder.inverse_transform(predicted_label_encoded)[0]
                results[model_name] = predicted_label

                PredictionHistory.objects.create(
                    text=new_text,
                    sentiment=predicted_label,
                    source=model_name,  # Salva o modelo usado no campo source
                    user=request.user if request.user.is_authenticated else None,
                    usuario_pessoa=usuario_pessoa
                )
            else:
                results[model_name] = "Modelo não encontrado"

        return JsonResponse({"text": new_text, "resultados": results})

    except Exception as e:
        return JsonResponse({"error": f"Erro ao processar o texto: {str(e)}"}, status=500)