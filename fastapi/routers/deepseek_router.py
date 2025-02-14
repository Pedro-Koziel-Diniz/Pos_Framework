import requests
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from utils import obter_logger_e_configuracao, DEEPSEEK_API_KEY, DEEPSEEK_API_URL

logger = obter_logger_e_configuracao()
router = APIRouter()

class SentimentRequest(BaseModel):
    text: str
    model: str = "deepseek-chat"

@router.post("/deepseek", summary="Análise de Sentimento com DeepSeek")
def classify_sentiment_deepseek_v1(request: SentimentRequest):
    """Classifica o sentimento usando a API da DeepSeek."""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": request.model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Analyze the sentiment of the following text and classify it as 'POSITIVO' for positive or 'NEGATIVO' for negative. "
                        "Respond with only 'POSITIVO' or 'NEGATIVO' and no additional text.\n\n"
                        f"Text: \"{request.text}\""
                    ),
                }
            ],
            "temperature": 0.2,
            "max_tokens": 10
        }

        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()

        if "choices" in response_data:
            sentiment = response_data["choices"][0]["message"]["content"].strip().upper()
            if sentiment in ["POSITIVO", "NEGATIVO"]:
                return {"text": request.text, "sentiment": sentiment}

        raise HTTPException(status_code=500, detail="Erro ao processar sentimento com DeepSeek")

    except Exception as e:
        logger.error(f"Erro ao processar sentimento com DeepSeek: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar sentimento com DeepSeek")