from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth.models import User


#Views relacionadas ao login e as autorizações
def login_user(request):#View que renderiza a tela de login
    return render(request, 'login.html')

def logout_user(request):#Redirecionamento para desautenticar o usuário atual
    logout(request)
    return redirect('/login/')


@csrf_protect
def submit_login(request):#Metodo de autenticação com lógica para checar se o usuário é um cliente,monitor ou superuser
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo = request.POST.get('tipos')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
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

#Views relacionadas ao CRUD do cliente
@login_required(login_url='/login/')
def index(request):#View retornado caso o login seja um cliente com uma lista dos pets cadastrado pelo cliente
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.filter(dono = cliente)
    return render(request, 'index.html',{'cliente':cliente,'pet':pet})

@login_required(login_url='/login/')
def pagina_cliente(request, id):#Tela renderizada para perfil do cliente, retornando do db(data base) as informações do cliente requerido pelo id e seus pets
    cliente = Cliente.objects.get(user = request.user, id=id)
    pet = Pet.objects.filter(dono = cliente)
    return render(request, 'cliente.html',{'pet':pet,'cliente':cliente})

@login_required(login_url='/login/')
def cliente_delete(request,id):#Metodo de deleção de cliente junto com o usuário criado para o mesmo
    cliente = Cliente.objects.get(user = request.user,id=id)
    user = request.user
    cliente.delete()
    user.delete()

    return redirect('/login/')

def register_cliente(request):#Metodo usado para a tela alteração ou criação de um cliente(alteração ocorre caso o cliente esteja autenticado)
    cliente_id = request.GET.get('id')
    if cliente_id:
        cliente = Cliente.objects.get(id = cliente_id)
        if cliente.user == request.user:
            return render(request, 'registro-cliente.html', {'cliente':cliente})
    return render(request, 'registro-cliente.html')

@login_required(login_url='/login/')
def leave_monitor(request):#Metodo de desvinculamento do monitor escolhido
    cliente = Cliente.objects.get(user = request.user)
    cliente.monitor_escolhido = None
    cliente.save()

    return redirect('/monitor-escolhido')

@login_required(login_url='/login/')
def monitor_escolhido(request):#Dados do monitor escolhido do cliente(enfase no contato)
    cliente = Cliente.objects.get(user = request.user)

    return render(request, 'monitor-escolhido.html',{'cliente':cliente})

@login_required(login_url='/login/')
def select_monitor(request,id):#Metodo de escolha de monitor caso o cliente não tenha um selecionado
    cliente = Cliente.objects.get(user = request.user)
    monitor = Monitor.objects.get(id=id)

    cliente.monitor_escolhido = monitor
    cliente.save()

    return redirect('/monitor-escolhido',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def link_monitor(request):#Metodo para renderizar todos os monitores disponíveis(cadastrados no banco de dados)
    cliente = Cliente.objects.get(user = request.user)
    monitor = Monitor.objects.all()

    return render(request, 'escolhe-monitor.html',{'cliente':cliente,'monitor':monitor})

def set_cliente(request):#Metodo onde as informações do front(template) de alteração(caso cliente autenticado) ou criação de cliente são aplicadas 
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

#Views relacionadas aos Pets
@login_required(login_url='/login/')
def register_pet(request):#Metodo para tela de alteração ou de criação de pets do cliente
    pet_id = request.GET.get('id')

    if pet_id:
        cliente = Cliente.objects.get(user = request.user)
        pet = Pet.objects.get(dono = cliente, id=pet_id)
        return render(request, 'registro-pet.html',{'cliente':cliente,'pet':pet})
    else:
        cliente = Cliente.objects.get(user = request.user)
        return render(request, 'registro-pet.html',{'cliente':cliente})

@login_required(login_url='/login/')
def set_pet(request):#Aplicação dos valores passados no front de alteração ou criação de pet 
    cliente = Cliente.objects.get(user = request.user)
    nome = request.POST.get('_nome_pet')
    tipo = request.POST.get('_tipo')
    pet_id = request.POST.get('pet-id')
    especie = request.POST.get('_especie')
    porte = request.POST.get('_porte')
    racao = request.POST.get('_racao')
    dono = cliente

    if pet_id:
        pet = Pet.objects.get(dono = cliente, id=pet_id)
        pet._nome_pet = nome
        pet._tipo = tipo
        pet._especie = especie
        pet._porte = porte
        pet._racao = racao

        pet.save()

        return redirect('/pet/datalhe/{}/'.format(pet.id))
    else:
        pet = Pet.objects.create(_nome_pet=nome,_tipo=tipo,_porte=porte,_especie=especie,_racao=racao,dono=dono)
        url = '/pet/datalhe/{}/'.format(pet.id)

        return redirect(url)

@login_required(login_url='/login/')
def pet_delete(request,id):#Metodo de deleção de pet de acordo com id
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(dono = cliente, id=id)
    pet.delete()

    return redirect('/')


@login_required(login_url='/login/')
def pet_detalhe(request,id):#Renderização de detalhes do pet selecionado pelo id
    cliente = Cliente.objects.get(user = request.user)
    pet = Pet.objects.get(dono = cliente, id =id)
    return render(request, 'pet.html',{'pet':pet,'cliente':cliente})

#views relacionadas ao CRUD de monitor
@login_required(login_url='/login/')
def monitor_page(request,id):#Página de perfil do monitor podendo alterar e deletar infos pessoais
    monitor = Monitor.objects.get(user = request.user, id=id)
    cliente = Cliente.objects.filter(monitor_escolhido = monitor)

    return render(request,'monitor-pagina.html',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def monitor_delete(request,id):#Metodo de deleção de monitor, evitando a deleção do cliente(gambiarra)
    monitor = Monitor.objects.get(user = request.user, id=id)
    cliente = Cliente.objects.filter(monitor_escolhido = monitor)
    user = request.user
    
    if cliente:
        for x in cliente:
            x.monitor_escolhido = None
            x.save()

    monitor.delete()
    user.delete()
    return redirect('/login/')

@login_required(login_url='/login/')
def monitor(request):#Metodo para renderizar o login do tipo monitor mostrando a lista dos clientes atrelados ao monitor
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.filter(monitor_escolhido = monitor)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'monitor.html',{'cliente':cliente,'monitor':monitor,'pet':pet})

@login_required(login_url='/login/')
def detalhe_cliente(request,id):#Metodo de descrição do cliente selecionado e a quantidade de pets que o mesmo tem
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(monitor_escolhido= monitor,id=id)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'meu-cliente.html',{'cliente':cliente,'pet':pet,'monitor':monitor})

@login_required(login_url='/login/')
def tudo_pet(request,id):#Mostra uma lista de pets do cliente selecionado
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(monitor_escolhido = monitor, id=id)
    pet = Pet.objects.filter(dono = cliente)

    return render(request, 'cliente-pets.html',{'cliente':cliente,'pet':pet,'monitor':monitor})

@login_required(login_url='/login/')
def hotel_pets(request):#Mostra todos os pets cadastrados no db, nome do dono e o monitor selecionado(sim, pode ser um que não esteja autenticado)
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.all()
    pet = Pet.objects.all()

    return render(request, 'todos-pets.html',{'pet':pet,'monitor':monitor,'cliente':cliente})

def register_monitor(request):#Pagina de alteração e criação do monitor
    monitor_id = request.GET.get('id')
    if monitor_id:
        monitor = Monitor.objects.get(id = monitor_id)
        if monitor.user == request.user:
            return render(request, 'registro-monitor.html',{'monitor':monitor})
    return render(request, 'registro-monitor.html')

@login_required(login_url='/login/')
def rel_cliente(request):#Metodo para lista de clientes disponíveis no db(clientes disponiveis = sem monitor)
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.filter(monitor_escolhido__isnull=True)

    return render(request, 'rel-cliente.html',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def select_cliente(request,id):#Metodo para atrelar o cliente a sua lista de clientes
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(id = id)

    cliente.monitor_escolhido = monitor
    cliente.save()

    return redirect('/monitor/',{'cliente':cliente,'monitor':monitor})

@login_required(login_url='/login/')
def leave_cliente(request,id):#Metodo para desvincular cliente da lista
    monitor = Monitor.objects.get(user = request.user)
    cliente = Cliente.objects.get(id =id)

    cliente.monitor_escolhido = None
    cliente.save()

    return redirect('/monitor/',{'cliente':cliente,'monitor':monitor})

def set_monitor(request):#Metodo em que os dados do front são passados ao db em caso de alteração ou criação de monitor
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
def cadastrar_servico(request):
    cliente_id = request.GET.get('id')
    if cliente_id:
        monitor = Monitor.objects.get(user = request.user)
        cliente = Cliente.objects.get(monitor_escolhido= monitor, id=cliente_id)
        pet = Pet.objects.filter(dono = cliente)

        return render(request, 'cadastro-servico.html',{'monitor':monitor,'cliente':cliente,'pet':pet})
    else:
        return redirect('/monitor/')

@login_required(login_url='/login/')
def post_servico(request):
    pet_id = request.POST.get('pet')
    nome = request.POST.get('nome')
    detalhes = request.POST.get('detalhes')
    monitor = Monitor.objects.get(user = request.user)
    pet = Pet.objects.get(id=pet_id)


    servico = Servicos.objects.create(_nome=nome,_detalhes=detalhes,pet=pet,monitor=monitor)
    return redirect('/logout/')