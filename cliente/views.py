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
    pet = Pet.objects.filter(dono = cliente)
    return render(request, 'index.html',{'cliente':cliente,'pet':pet})

@login_required(login_url='/login/')
def register_pet(request):
    pet_id = request.GET.get('id')

    if pet_id:
        cliente = Cliente.objects.get(user = request.user)
        pet = Pet.objects.get(dono = cliente, id=pet_id)
        return render(request, 'registro-pet.html',{'cliente':cliente,'pet':pet})
    else:
        cliente = Cliente.objects.get(user = request.user)
        return render(request, 'registro-pet.html',{'cliente':cliente})

@login_required(login_url='/login/')
def set_pet(request):
    cliente = Cliente.objects.get(user = request.user)
    nome = request.POST.get('_nome_pet')
    tipo = request.POST.get('_tipo')
    pet_id = request.POST.get('pet-id')
    especie = request.POST.get('_especie')
    porte = request.POST.get('_porte')
    racao = request.POST.get('_racao')
    servicos = request.POST.get('_servicos')
    dono = cliente

    if pet_id:
        pet = Pet.objects.get(dono = cliente, id=pet_id)
        pet._nome_pet = nome
        pet._tipo = tipo
        pet._especie = especie
        pet._porte = porte
        pet._racao = racao
        pet._servicos = servicos

        pet.save()

        return redirect('/pet/datalhe/{}/'.format(pet.id))
    else:
        pet = Pet.objects.create(_nome_pet=nome,_tipo=tipo,_porte=porte,_especie=especie,_racao=racao,dono=dono,_servicos=servicos)
        url = '/pet/datalhe/{}/'.format(pet.id)

        return redirect(url)

@login_required(login_url='/login/')
def pet_delete(request,id):
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(dono = cliente, id=id)
    pet.delete()

    return redirect('/')


@login_required(login_url='/login/')
def pet_detalhe(request,id):
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(dono = cliente, id =id)
    return render(request, 'pet.html',{'pet':pet,'cliente':cliente})

@login_required(login_url='/login/')
def pagina_cliente(request, id):
    cliente = Cliente.objects.get(user = request.user, id=id)
    pet = Pet.objects.filter(dono = cliente)
    return render(request, 'cliente.html',{'pet':pet,'cliente':cliente})

@login_required(login_url='/login/')
def cliente_delete(request,id):
    cliente = Cliente.objects.get(user = request.user,id=id)
    user = request.user
    cliente.delete()
    user.delete()

    return redirect('/login/')

@login_required(login_url='/login/')
def monitor(request):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.filter(monitor_escolhido = monitor)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'monitor.html',{'cliente':cliente,'monitor':monitor,'pet':pet})

@login_required(login_url='/login/')
def detalhe_cliente(request,id):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(monitor_escolhido= monitor,id=id)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'meu-cliente.html',{'cliente':cliente,'pet':pet,'monitor':monitor})

@login_required(login_url='/login/')
def tudo_pet(request,id):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(monitor_escolhido = monitor, id=id)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'cliente-pets.html',{'cliente':cliente,'pet':pet,'monitor':monitor})

@login_required(login_url='/login/')
def hotel_pets(request):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.all()
    pet = Pet.objects.all()

    return render(request, 'todos-pets.html',{'pet':pet,'monitor':monitor,'cliente':cliente})

def logout_user(request):
    logout(request)
    return redirect('/login/')


def login_user(request):
    return render(request, 'login.html')

def register_cliente(request):
    cliente_id = request.GET.get('id')
    if cliente_id:
        cliente = Cliente.objects.get(id = cliente_id)
        if cliente.user == request.user:
            return render(request, 'registro-cliente.html', {'cliente':cliente})
    return render(request, 'registro-cliente.html')

@login_required(login_url='/login/')
def monitor_escolhido(request):
    cliente = Cliente.objects.get(user = request.user)

    return render(request, 'monitor-escolhido.html',{'cliente':cliente})

@login_required(login_url='/login/')
def leave_monitor(request):
    cliente = Cliente.objects.get(user = request.user)
    cliente.monitor_escolhido = None
    cliente.save()

    return redirect('/monitor-escolhido')

def register_monitor(request):
    monitor_id = request.GET.get('id')
    if monitor_id:
        monitor = Monitor.objects.get(id = monitor_id)
        if monitor.user == request.user:
            return render(request, 'registro-monitor.html',{'monitor':monitor})
    return render(request, 'registro-monitor.html')

@login_required(login_url='/login/')
def rel_cliente(request):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.filter(monitor_escolhido__isnull=True)

    return render(request, 'rel-cliente.html',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def select_cliente(request,id):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(id = id)

    cliente.monitor_escolhido = monitor
    cliente.save()

    return redirect('/monitor/',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def leave_cliente(request,id):
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(id =id)

    cliente.monitor_escolhido = None
    cliente.save()

    return redirect('/monitor/',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def select_monitor(request,id):
    cliente = Cliente.objects.get(user = request.user)
    monitor = Monitor.objects.get(id=id)

    cliente.monitor_escolhido = monitor
    cliente.save()

    return redirect('/monitor-escolhido',{'cliente':cliente,'monitor':monitor})

def set_monitor(request):
    username = request.POST.get('username')
    nome = request.POST.get('_nome')
    cpf = request.POST.get('_CPF')
    monitor_id = request.POST.get('monitor-id')
    email = request.POST.get('_email')
    tel = request.POST.get('_tel')
    CTPS = request.POST.get('_CTPS')

    if monitor_id:
        monitor = Monitor.objects.get(id = monitor_id)
        if request.user == cliente.user:
            monitor.email = email
            monitor.nome = nome
            monitor.CPF = cpf
            monitor.user.username = username
            monitor.CTPS = CTPS
            if request.POST.get('password') == request.POST.get('Cpassword'):
                password = request.POST.get('password')
                monitor.user.set_password(password)
                monitor.user.save()
                monitor.save()
                return redirect('/')
            else:
                messages.error(request, 'Senhas não se coincidem')
        return redirect('/')
    else:
        if request.POST.get('password') == request.POST.get('Cpassword'):
            password = request.POST.get('password')
            user = User.objects.create(username=username,password=password,email=email)
            user.set_password(password)
            user.save()
            monitor = Monitor.objects.create(_CPF=cpf,_nome=nome,_email=email,_tel=tel,user=user,_CTPS=CTPS)
            return redirect('/login/')
        else:
            messages.error(request, 'Senhas não se coincidem')
        return redirect('/novo-monitor/')

@login_required(login_url='/login/')
def monitor_page(request,id):
    monitor = Monitor.objects.get(user = request.user, id=id)
    cliente = Cliente.objects.filter(monitor_escolhido = monitor)

    return render(request,'monitor-pagina.html',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def link_monitor(request):
    cliente = Cliente.objects.get(user = request.user)
    monitor = Monitor.objects.all()

    return render(request, 'escolhe-monitor.html',{'cliente':cliente,'monitor':monitor})


def set_cliente(request):
    username = request.POST.get('username')
    nome = request.POST.get('_nome')
    cpf = request.POST.get('_CPF')
    cliente_id = request.POST.get('cliente-id')
    email = request.POST.get('_email')
    tel = request.POST.get('_tel')

    if cliente_id:
        cliente = Cliente.objects.get(id = cliente_id)
        if request.user == cliente.user:
            cliente.email = email
            cliente.nome = nome
            cliente.CPF = cpf
            cliente.user.username = username
            if request.POST.get('password') == request.POST.get('Cpassword'):
                password = request.POST.get('password')
                cliente.user.set_password(password)
                cliente.user.save()
                cliente.save()
                return redirect('/')
            else:
                messages.error(request, 'Senhas não se coincidem')
        return redirect('/')
    else:
        if request.POST.get('password') == request.POST.get('Cpassword'):
            password = request.POST.get('password')
            user = User.objects.create(username=username,password=password,email=email)
            user.set_password(password)
            user.save()
            cliente = Cliente.objects.create(_CPF=cpf,_nome=nome,_email=email,_tel=tel,user=user)
            return redirect('/login/')
        else:
            messages.error(request, 'Senhas não se coincidem')
        return redirect('/novo-cliente/')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo = request.POST.get('tipos')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print(type(user))
            print(type(request.user))
            if request.user.is_superuser:
                return redirect('/admin/')
            else:
                if hasattr(user,'cliente'):
                    return redirect('/')
                elif hasattr(user,'monitor'):
                    return redirect('/monitor/')
        else:
            messages.error(request, 'Campos não existentes ou incorretos')
    return redirect('/login/')