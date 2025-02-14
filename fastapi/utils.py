import os
import openai
import joblib
import logging
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Configuração da API DeepSeek
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# Diretórios de modelos
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_DIR, "machine_learning", "models")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

# Carregar modelos ML
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def obter_logger_e_configuracao():
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    return logging.getLogger("fastapi")

def commom_verificacao_api_token(api_token: str):
    API_TOKEN = os.getenv("API_TOKEN")
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")


