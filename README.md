# Pós Agentes Inteligentes - FRAMEWORK DE DESENVOLVIMENTO WEB P/ CONSUMO DE MODELOS TREI. INTELIGÊNCIA ARTIFICIAL

Repositório dedicado para o trabalho final desenvolvido na disciplina de FRAMEWORK DE DESENVOLVIMENTO WEB P/ CONSUMO DE MODELOS TREI. INTELIGÊNCIA ARTIFICIAL, da pós graduação de Agentes Inteligentes, pela UFG.

Integrantes: Marcos Vinicius, Pedro Koziel e Wagner Filho.

## Descrição do trabalho

Construir um site, aplicação (web/internet - Django), de forma que haja (i) carregamento de dados (ex: csv, excel, etc.), (ii) uso de algoritmo de IA, e (iii) mostrar os resultados em tela.
          - Implementação de algoritmos de classificação de sentimentos utilizando modelos baseados em aprendizado de máquina e API da OpenAI para classificação dos textos.
          - Otimização de hiperparâmetros e testes com diferentes modelos de machine learning.
          - Desenvolvimento de uma interface para interação com os modelos e visualização dos resultados.
          - Criação de um banco de dados para armazenar e gerenciar o histórico de análises realizadas.

# Projeto Final


Siga as instruções abaixo para garantir uma instalação e execução corretas.

---

## **1. Requisitos do Sistema**

Certifique-se de que os seguintes componentes estejam instalados no sistema:

- **Python 3.9 ou superior**
- **pip** (gerenciador de pacotes do Python)
- **Virtualenv** (opcional, mas recomendado para isolar o ambiente do projeto)
---

## **2. Configuração do Ambiente**

### **Passo 1: Clonar o Repositório**

Clone o repositório do projeto para sua máquina local:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
```

### **Passo 2: Criar e Ativar um Ambiente Virtual**

Crie um ambiente virtual para o projeto:
```bash
python3 -m venv venv
```

Ative o ambiente virtual:
- No Linux/Mac:
  ```bash
  source venv/bin/activate
  ```
- No Windows:
  ```bash
  venv\Scripts\activate
  ```

### **Passo 3: Instalar Dependências**

Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## **4. Criar um Superusuário**

Crie um superusuário para acessar a área administrativa do Django:
```bash
python manage.py createsuperuser
```
Durante o processo, você precisará fornecer as seguintes informações:
- Email
- Nome de usuário
- Nome e sobrenome
- Senha


Crie as tabelas no banco de dados:
```bash
python manage.py migrate
```

---

## **5. Executar o Servidor de Desenvolvimento**

Inicie o servidor de desenvolvimento do Django:
```bash
python manage.py runserver
```

Acesse o projeto no navegador em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## **6. Acessar a Administração do Django**

Para acessar o painel administrativo, entre no seguinte link:
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Use o email e a senha criados para o superusuário.

---
