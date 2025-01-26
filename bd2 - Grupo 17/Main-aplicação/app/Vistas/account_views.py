from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from ..Database.Utilizador import create_utilizador  # Importando a função de criação
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test

import logging



def home(request):
    # Aqui você pode verificar se o usuário está autenticado ou qualquer outra lógica
    if not request.user.is_authenticated:
        return redirect('login')  # Redireciona para a página de login se não estiver autenticado
    return render(request, 'home.html')  # Ou renderiza a página inicial se estiver autenticado

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina_inicial')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    return render(request, 'Login/Login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de login

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        telefone = request.POST.get('telefone', '')  # Captura do telefone (se fornecido)
        tipo_utilizador = 'cliente'  # Ou 'admin', dependendo da lógica do seu sistema

        # Verificar se as senhas coincidem
        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'register.html')

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'O nome de usuário já está em uso.')
            return render(request, 'register.html')

        # Verificar se o email já está em uso
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return render(request, 'register.html')

        # Criar o usuário na tabela 'auth_user'
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Criar o utilizador na tabela personalizada 'utilizador_bd2'
        data_criacao = timezone.now()  # Pega a data e hora atual
        try:
            create_utilizador(
                nome=user.username,  # Nome será o nome de usuário
                email=user.email,
                telefone=telefone,
                tipo_utilizador=tipo_utilizador,
                data_criacao=data_criacao,
            )
            messages.success(request, 'Conta criada com sucesso. Faça login agora!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar no banco de dados: {str(e)}')

        return redirect('login')

    return render(request, 'Login/Register.html')

# Função para verificar se o usuário é do tipo "staff"
def user_is_staff(user):
    return user.is_staff

# View para a página que só pode ser acessada por admins (staff)
@login_required
@user_passes_test(user_is_staff)
def homepage(request):
    # Esta página será acessível apenas por usuários com is_staff = True
    return render(request, 'navbar.html')


@login_required
def perfil(request):
    return render(request, 'Login/Perfil.html', {
        'user': request.user,
    })
