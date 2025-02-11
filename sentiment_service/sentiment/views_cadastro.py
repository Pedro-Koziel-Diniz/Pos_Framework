from django.shortcuts import render, redirect
from django.contrib import messages
from .models_cadastro import pessoa
import uuid

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        funcao = request.POST.get('funcao')
        nascimento = request.POST.get('nascimento')

        if pessoa.objects.filter(email=email).exists():
            messages.error(request, "E-mail já cadastrado. Utilize outro e-mail.")
            return redirect('cadastro')
        
        token_gerado = str(uuid.uuid4().hex)
        
        nova_pessoa = pessoa(
            nome=nome,
            usuario=usuario,
            senha=senha,
            email=email,
            celular=celular,
            funcao=funcao,
            nascimento=nascimento,
            token=token_gerado
        )
        nova_pessoa.save()

        messages.success(request, f'Usuário {nome} cadastrado com sucesso!')
        return redirect('index')

    return render(request, 'sentiment/cadastro.html')
