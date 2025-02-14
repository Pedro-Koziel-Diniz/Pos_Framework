from django.http import JsonResponse
from .models_cadastro import pessoa
import functools

def authenticate_request(request):
    """
    Verifica se o usuário está autenticado via sessão (Web) ou via token (API).
    Retorna um objeto do modelo `pessoa` se autenticado, caso contrário retorna None.
    """
    # **1️⃣ Primeiro, verifica se o usuário está autenticado na sessão (Web)**
    if request.session.get('username'):
        try:
            usuario = pessoa.objects.get(usuario=request.session.get('username'))
            return usuario  # Retorna o usuário autenticado do modelo `pessoa`
        except pessoa.DoesNotExist:
            return None

    # **2️⃣ Se não estiver autenticado via sessão, tenta autenticação via token**
    token = request.headers.get('Authorization')
    if token:
        try:
            usuario = pessoa.objects.get(token=token)
            return usuario  # Retorna o usuário autenticado do modelo `pessoa`
        except pessoa.DoesNotExist:
            return None

    return None  # Nenhum método de autenticação foi bem-sucedido

def authentication_required(view_func):
    """ 
    Decorador para verificar se o usuário está autenticado via Web ou API Token
    e possui permissão para acessar a API.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        usuario = authenticate_request(request)  # Tenta autenticar o usuário

        if not usuario:
            return JsonResponse({'error': 'Autenticação necessária. Faça login ou forneça um token válido.'}, status=401)

        # **Verifica se o usuário tem alguma permissão para acessar a API**
        if not (usuario.permissao_sentiment_gpt or usuario.permissao_sentiment_deepseek or usuario.permissao_sentiment_ml):
            return JsonResponse({'error': 'Usuário sem permissão de acesso à API.'}, status=403)

        request.pessoa = usuario  # Armazena o usuário autenticado no `request.pessoa`
        return view_func(request, *args, **kwargs)  # Executa a função original

    return wrapper
