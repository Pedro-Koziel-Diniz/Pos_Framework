from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils import commom_verificacao_api_token, obter_logger_e_configuracao
from routers import gpt_router, ml_router, deepseek_router

logger = obter_logger_e_configuracao()

description = """
API para Análise de Sentimentos utilizando modelos de Machine Learning e LLMs via OpenAI (GPT) e DeepSeek.

## Endpoints (versão 1):

- `/v1/sentiment/ml` → Classificação com Modelos de Machine Learning
- `/v1/sentiment/gpt` → Classificação com API da OpenAI (GPT)
- `/v1/sentiment/deepseek` → Classificação com API da DeepSeek
"""

app = FastAPI(
    title="API de Análise de Sentimentos",
    description=description,
    version="1.0",
    contact={
        "name": "Marcos Vinicius, Pedro Koziel e Wagner Filho.",
        "url": "https://github.com/Pedro-Koziel-Diniz/Pos_Framework",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    dependencies=[Depends(commom_verificacao_api_token)],
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modifique para restringir acesso em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar os routers dentro da versão v1
app.include_router(ml_router.router, prefix="/v1/sentiment")
app.include_router(gpt_router.router, prefix="/v1/sentiment")
app.include_router(deepseek_router.router, prefix="/v1/sentiment")

@app.get("/")
def root():
    return {"message": "Sentiment Analysis API is running"}

@app.get("/", dependencies=[Depends(commom_verificacao_api_token)], tags=["Root"])
def root():
    """Endpoint raiz protegido por API Token"""
    return {"message": "Sentiment Analysis API is running!"}

@app.get("/health", dependencies=[Depends(commom_verificacao_api_token)], tags=["Health Check"])
def health_check():
    """Verifica o status da API"""
    logger.info("Health check solicitado")
    return {"status": "ok"}
