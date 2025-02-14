from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models_cadastro import pessoa
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models_cadastro import pessoa

@csrf_exempt
def obter_token(request):
    """ Retorna o token do usuário com base no usuário e senha e armazena na sessão """
    if request.method == 'POST':
        try:
            # 🛠️ Garante que o corpo da requisição não está vazio antes de decodificar JSON
            if not request.body:
                return JsonResponse({'error': 'Corpo da requisição vazio'}, status=400)

            data = json.loads(request.body.decode('utf-8'))  # 🛠️ Decodifica corretamente o JSON

            usuario = data.get('usuario')
            senha = data.get('senha')

            if not usuario or not senha:
                return JsonResponse({'error': 'Usuário e senha são obrigatórios'}, status=400)

            # Busca a pessoa com base no usuário e senha
            user = pessoa.objects.get(usuario=usuario, senha=senha)

            # Armazena o usuário na sessão
            request.session['username'] = usuario
            request.session.save()

            return JsonResponse({'token': user.token})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erro ao decodificar JSON. Verifique a estrutura da requisição.'}, status=400)

        except pessoa.DoesNotExist:
            return JsonResponse({'error': 'Usuário ou senha incorretos'}, status=401)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

def token_view(request):
    """ Exibe o nome do usuário logado e seu token """
    usuario = request.session.get('username')  # Obtém o usuário armazenado na sessão (Corrigido)

    if not usuario:
        return redirect('/login/')  # Redireciona para login se não estiver autenticado

    try:
        user = pessoa.objects.get(usuario=usuario)
        token = user.token
    except pessoa.DoesNotExist:
        token = "Token não encontrado"

    return render(request, 'sentiment/token.html', {'usuario': usuario, 'token': token})