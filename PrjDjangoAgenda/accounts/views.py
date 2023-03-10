from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario: str = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, 'Campos invalidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Logado')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome: str = request.POST.get('nome')
    sobrenome: str = request.POST.get('sobrenome')
    email: str = request.POST.get('email')
    usuario: str = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'As campos nao podem ser vazio')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.add_message(request, messages.ERROR, 'Senha invalido')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.add_message(request, messages.ERROR, 'Usuario invalido')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Senhas nao iguais')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, 'Usuario ja existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Email ja existe')
        return render(request, 'accounts/cadastro.html')

    messages.add_message(request, messages.SUCCESS, 'Sucesso')

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.add_message(request, messages.WARNING, 'Erro ao enviar')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')
    if len(descricao) < 5:
        messages.add_message(request, messages.WARNING, 'Descricao precisa ter mais que 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    messages.add_message(request, messages.SUCCESS, f'Salvo {request.POST.get("nome")}')
    form.save()
    return redirect('dashboard')
