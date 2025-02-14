import os
import openai
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from utils import obter_logger_e_configuracao

logger = obter_logger_e_configuracao()
router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

@router.post("/gpt", summary="Análise de Sentimento com OpenAI GPT")
def classify_sentiment_gpt_v1(request: SentimentRequest):
    """Classifica o sentimento usando o modelo GPT da OpenAI"""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analyze the sentiment of the following text and classify it as 'POSITIVO' for positive or 'NEGATIVO' for negative. "
                        f"Respond with only 'POSITIVO' or 'NEGATIVO' and no additional text.\n\n"
                        f"Text: \"{request.text}\""
                    ),
                }
            ],
        )

        sentiment = response["choices"][0]["message"]["content"].strip().upper()
        if sentiment not in ["POSITIVO", "NEGATIVO"]:
            sentiment = "INVÁLIDO"

        return {"text": request.text, "sentiment": sentiment}

    except Exception as e:
        logger.error(f"Erro ao processar sentimento com GPT: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar sentimento com GPT")