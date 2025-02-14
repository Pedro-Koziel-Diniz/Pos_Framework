# API de Análise de Sentimentos utilizando framework FastAPI

Esta API permite classificar o sentimento de um texto de entrada utilizando diferentes abordagens:

**OpenAI GPT** - Usa o modelo `gpt-4o-mini` para classificação  
**Machine Learning** - Usa modelos tradicionais de ML treinados  
**DeepSeek AI** - Usa a API da DeepSeek para análise de sentimentos  

A API segue um **versionamento estruturado** (`/v1/sentiment/...`) para facilitar futuras atualizações.

---

### Configuração de variáveis de ambiente
Crie um arquivo .env na raiz do projeto e defina as seguintes variáveis:
```sh
API_TOKEN=seu_token
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

Com o ambiente virtual criado e instaladas as dependências

Caso esteja usando Machine Learning, garanta que os arquivos dos modelos estejam na pasta correta.

### Como Rodar a API
- Executar a API em ambiente de desenvolvimento: `fastapi dev main.py`
- Executar a API em ambiente de produção: `fastapi run main.py`
- A API estará disponível em: http://127.0.0.1:8000
- Acesse a rota `/docs` para documentação interativa utilizando Swagger UI ou `/redoc` para documentação no formato ReDoc.

### Exemplo de Requisição:
```sh
{
  "text": "Eu estou muito feliz com esse serviço!"
}
```

Resposta Esperada:

```sh
{
  "text": "Eu estou muito feliz com esse serviço!",
  "sentiment": "POSITIVO"
}
```

