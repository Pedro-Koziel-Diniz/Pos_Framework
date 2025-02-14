import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .authentication import authentication_required
from .models_sentiment import PredictionHistory
from .views_ml import predict_sentiment  # Modelos ML
from .views_gpt import classify_sentiment_gpt  # Modelo GPT
from .views_deepseek import classify_sentiment_deepseek  # Modelo DeepSeek

# Modelos disponíveis para Sentiment ML
MODELOS_ML = ["KNN", "LinearSVC", "LogisticRegression", "MultinomialNB", "RandomForest"]

@csrf_exempt
@authentication_required
def predict_sentiment_api(request):
    """
    API que recebe um texto via POST e retorna a análise de sentimento.
    Apenas usuários com permissão podem acessar modelos específicos.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Lê o JSON recebido
            text = data.get("text", "").strip()
            models = data.get("models", [])  # Modelos solicitados pelo usuário

            if not text:
                return JsonResponse({"error": "Texto não fornecido"}, status=400)

            # **Verifica a permissão do usuário**
            usuario_pessoa = request.pessoa  # Obtido via `authentication_required`

            # **Define quais modelos ele pode acessar**
            modelos_permitidos = set()
            if usuario_pessoa.permissao_sentiment_gpt:
                modelos_permitidos.add("GPT")
            if usuario_pessoa.permissao_sentiment_deepseek:
                modelos_permitidos.add("DeepSeek")
            if usuario_pessoa.permissao_sentiment_ml:
                modelos_permitidos.update(MODELOS_ML)

            # **Se o usuário não especificou modelos, usa os permitidos**
            if not models:
                models = list(modelos_permitidos)

            # **Verifica se o usuário tentou acessar modelos não permitidos**
            modelos_invalidos = [m for m in models if m not in modelos_permitidos]

            if modelos_invalidos:
                return JsonResponse({
                    "error": "Você não tem permissão para acessar os seguintes modelos:",
                    "modelos_invalidos": modelos_invalidos
                }, status=403)

            # **Processar os modelos solicitados**
            resultados = {}

            for model in models:
                if model in MODELOS_ML:
                    # **Chama a função existente `predict_sentiment` para modelos ML**
                    request.GET = request.GET.copy()
                    request.GET["text"] = text
                    request.GET["models"] = model

                    response = predict_sentiment(request)
                    response_data = json.loads(response.content.decode('utf-8'))
                    resultados.update(response_data.get("resultados", {}))

                elif model == "GPT":
                    # **Chama a função `classify_sentiment_gpt` para GPT**
                    sentiment = classify_sentiment_gpt(text)
                    sentiment = (
                        "NEGATIVO" if sentiment == "neg" else
                        "POSITIVO" if sentiment == "pos" else "INVÁLIDO"
                    )
                    resultados["GPT"] = sentiment

                elif model == "DeepSeek":
                    # **Chama a função `classify_sentiment_deepseek` para DeepSeek**
                    sentiment = classify_sentiment_deepseek(text)

                    # **Se o erro for "Insufficient Balance", retorna erro 402**
                    if sentiment == "Insufficient Balance":
                        return JsonResponse(
                            {'error': 'Saldo insuficiente para consulta na API DeepSeek.'}, 
                            status=402
                        )

                    if sentiment is None:
                        return JsonResponse(
                            {'error': 'Erro ao processar sentimento com DeepSeek'}, 
                            status=500
                        )

                    sentiment = (
                        "NEGATIVO" if sentiment == "neg" else
                        "POSITIVO" if sentiment == "pos" else "INVÁLIDO"
                    )
                    resultados["DeepSeek"] = sentiment

            # **Salva no histórico**
            for model_name, sentiment in resultados.items():
                PredictionHistory.objects.create(
                    text=text,
                    sentiment=sentiment,
                    source=model_name,
                    usuario_pessoa=usuario_pessoa
                )

            return JsonResponse({"text": text, "resultados": resultados})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Erro ao decodificar JSON. Verifique a estrutura da requisição."}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)
