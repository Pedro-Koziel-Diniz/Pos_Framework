import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openai
from dotenv import load_dotenv
from wordcloud import WordCloud
from PIL import Image
from nltk.corpus import stopwords
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# Carregar variáveis do .env
load_dotenv()

# Configurar a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

 #Importar todo conjunto de dados
df = pd.read_csv('data/imdb-reviews-pt-br.csv', index_col='id')
_, df1 = train_test_split(df, test_size=5, random_state=42, shuffle=True)

def classify_sentiment_gpt(content, model="gpt-4o-mini"):
    """
    Usa o modelo OpenAI Chat para classificar o sentimento de um texto.
    Retorna apenas 'pos' ou 'neg'.
    """
    try:
        # Fazer a chamada à API
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
        # Extrair a resposta do modelo
        return response["choices"][0]["message"]["content"].strip().lower()
    except Exception as e:
        print(f"Error processing text: {content}\n{e}")
        return None

# Classificar o sentimento de cada texto no DataFrame
df1['sentiment_llm_en'] = df1['text_en'].apply(lambda x: classify_sentiment_gpt(x))
# Exibir os resultados
print(df1)
