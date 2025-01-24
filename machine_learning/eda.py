import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from nltk.corpus import stopwords
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from tqdm.notebook import tqdm
tqdm.pandas()

 #Importar todo conjunto de dados
df = pd.read_csv('data/imdb-reviews-pt-br.csv', index_col='id')
# Obter amostra de tamanho 100
_, df = train_test_split(df, test_size=200, random_state=42, shuffle=True)

# Contagem absoluta
contagem_absoluta = df['sentiment'].value_counts()

# Contagem relativa
contagem_relativa = df['sentiment'].value_counts(normalize=True) * 100

# Criar gráfico de barras
fig, ax = plt.subplots(figsize=(6, 4))
barras = plt.bar(contagem_absoluta.index, contagem_absoluta, color=['green', 'red'])

# Adicionar texto nas barras
for barra, abs_value, rel_value in zip(barras, contagem_absoluta, contagem_relativa):
    yval = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2, yval, f'{abs_value} ({rel_value:.1f}%)',
            ha='center', va='bottom', color='black', fontsize=12)

# Adicionar rótulos e título
plt.xlabel('Sentimento', fontsize=14)
plt.ylabel('Frequência absoluta', fontsize=14)
plt.title('Quantidade de textos de cada sentimento \nem uma amostra de tamanho 200', fontsize=16, x=0.5, y=1.1)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Remover bordas da parte superior e direita
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Ajustar layout
plt.tight_layout()

# Salvar imagem
plt.savefig(f"img/freq_sentiment.png", bbox_inches='tight')

# Exibir o gráfico
#plt.show()

def generate_wordcloud(df, language='en'):
    # Definir stopwords para o idioma escolhido
    if language == 'en':
        stop_words_pos = stop_words_neg = set(stopwords.words('english'))
        stop_words_pos.update(["film", "movie", "one"])
        stop_words_neg.update(["character", "like", "really", "make", "see"])
    elif language == 'pt':
        stop_words_pos = stop_words_neg = set(stopwords.words('portuguese'))
        stop_words_pos.update(["filme", "filmes", "todo", "tão", "pode", "todos"])
        stop_words_neg.update(["filme", "filmes", "todo", "tão", "filme", "coisa", "realmente"])
    else:
        raise ValueError("Language must be 'en' or 'pt'.")

    # Concatenar textos positivos e negativos
    txt_pos = " ".join(review for review in df[df.sentiment == 'pos'][f'text_{language}'])
    txt_neg = " ".join(review for review in df[df.sentiment == 'neg'][f'text_{language}'])

    # Carregar máscaras de imagem
    mask_pos = None
    mask_neg = None

    # Gerar nuvens de palavras positivas e negativas
    wordcloud_positivo = WordCloud(
        stopwords=stop_words_pos,
        random_state=42,
        background_color="white",
        color_func=lambda *args, **kwargs: "green",
        contour_color='black',
        contour_width=1,
        max_font_size=100,
        min_font_size=15,
        max_words=200,
        mask=mask_pos
    ).generate(txt_pos)

    wordcloud_negativo = WordCloud(
        stopwords=stop_words_neg,
        random_state=42,
        background_color="white",
        color_func=lambda *args, **kwargs: "red",
        contour_color='black',
        contour_width=1,
        max_font_size=100,
        min_font_size=15,
        max_words=200,
        mask=mask_neg
    ).generate(txt_neg)

    # Configurações do plot
    plt.figure(figsize=(7, 14))

    # Plotar nuvem de palavras positivas
    plt.subplot(1, 2, 1)
    plt.imshow(wordcloud_positivo, interpolation='bilinear')
    plt.axis('off')
    plt.title('Positivo', fontsize=20, color='green')

    # Plotar nuvem de palavras negativas
    plt.subplot(1, 2, 2)
    plt.imshow(wordcloud_negativo, interpolation='bilinear')
    plt.axis('off')
    plt.title('Negativo', fontsize=20, color='red')

    # Ajustar layout
    plt.tight_layout()

    # Salvar a nuvem de palavras como imagem
    plt.savefig(f"img/wordcloud_{language}.png", bbox_inches='tight')

    # Exibir a nuvem de palavras
    #plt.show()
    
# Exemplo de uso para o idioma inglês
generate_wordcloud(df, language='en')

# Exemplo de uso para o idioma português
generate_wordcloud(df, language='pt')
