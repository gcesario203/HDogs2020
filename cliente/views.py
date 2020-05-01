from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def index(request):
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.filter(_dono = cliente)
    return render(request, 'index.html',{'cliente':cliente,'pet':pet})

@login_required(login_url='/login/')
def register_pet(request):
    cliente = Cliente.objects.get(user = request.user)
    return render(request, 'registro-pet.html',{'cliente':cliente})

@login_required(login_url='/login/')
def set_pet(request):
    cliente = Cliente.objects.get(user = request.user)
    nome = request.POST.get('_nome_pet')
    tipo = request.POST.get('_tipo')
    especie = request.POST.get('_especie')
    porte = request.POST.get('_porte')
    racao = request.POST.get('_racao')
    servicos = request.POST.get('_servicos')
    dono = cliente

    pet = Pet.objects.create(_nome_pet=nome,_tipo=tipo,_porte=porte,_especie=especie,_racao=racao,_dono=dono,_servicos=servicos)
    url = '/pet/datalhe/{}/'.format(pet.id)

    return redirect(url)

@login_required(login_url='/login/')
def pet_delete(request,id):
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(_dono = cliente, id=id)
    pet.delete()

    return redirect('/')


@login_required(login_url='/login/')
def pet_detalhe(request,id):
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(_dono = cliente, id =id)
    return render(request, 'pet.html',{'pet':pet,'cliente':cliente})

def logout_user(request):
    print(request.user)
    logout(request)
    return redirect('/login/')


def login_user(request):
    return render(request, 'login.html')

def register_cliente(request):
    return render(request, 'registro-cliente.html')

def set_cliente(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    nome = request.POST.get('_nome')
    cpf = request.POST.get('_CPF')
    email = request.POST.get('_email')
    tel = request.POST.get('_tel')

    user = User.objects.create(username=username,password=password,email=email)
    user.set_password(password)
    user.save()
    cliente = Cliente.objects.create(_CPF=cpf,_nome=nome,_email=email,_tel=tel,user=user)

    return redirect('/login/')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/')
        else:
            messages.error(request, 'Campos não existentes ou incorretos')
    return redirect('/login/')