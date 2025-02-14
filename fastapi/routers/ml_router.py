import os
import joblib
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from utils import obter_logger_e_configuracao, MODEL_DIR, vectorizer, label_encoder

logger = obter_logger_e_configuracao()
router = APIRouter()

class SentimentRequest(BaseModel):
    text: str
    model: str = "LogisticRegression"

@router.post("/ml", summary="Análise de Sentimento com Modelos de Machine Learning")
def predict_sentiment_v1(request: SentimentRequest):
    """Classifica o sentimento usando um dos modelos de Machine Learning treinados:
        - LogisticRegression
        - MultinomialNB
        - RandomForest
        - LinearSVC
        - KNN
    """
    try:
        new_text_tfidf = vectorizer.transform([request.text])
        model_path = os.path.join(MODEL_DIR, f"{request.model}.pkl")

        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Modelo não encontrado")

        classifier = joblib.load(model_path)
        predicted_label_encoded = classifier.predict(new_text_tfidf)
        predicted_label = label_encoder.inverse_transform(predicted_label_encoded)[0].upper()

        return {"text": request.text, "sentiment": predicted_label}

    except Exception as e:
        logger.error(f"Erro ao processar texto com modelo ML: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar sentimento com ML")