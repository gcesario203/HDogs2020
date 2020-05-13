"""hdogs URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/3.0/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cliente import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user),
    path('pet/datalhe/<id>/', views.pet_detalhe),
    path('pet/register/', views.register_pet),
    path('pet/register/submit', views.set_pet),
    path('pet/delete/<id>/', views.pet_delete),
    path('login/submit', views.submit_login),
    path('novo-cliente/', views.register_cliente),
    path('minha-pagina/<id>', views.pagina_cliente),
    path('minha-pagina/delete/<id>', views.cliente_delete),
    path('monitor-escolhido', views.monitor_escolhido),
    path('monitor-escolhido/leave-monitor', views.leave_monitor),
    path('novo-cliente/submit', views.set_cliente),
    path('logout/', views.logout_user),
    path('novo-monitor/', views.register_monitor),
    path('novo-monitor/submit', views.set_monitor),
    path('monitor/', views.monitor),
    path('monitor/<id>', views.monitor_page),
    path('monitor/delete/<id>', views.monitor_delete),
    path('rel_cliente', views.rel_cliente),
    path('rel_cliente/<id>', views.select_cliente),
    path('monitor/leave_cliente/<id>', views.leave_cliente),
    path('monitores-disponiveis/', views.link_monitor),
    path('monitores-disponiveis/<id>/select',views.select_monitor),
    path('meu-cliente/<id>', views.detalhe_cliente),
    path('meu-cliente/<id>/pets/', views.tudo_pet),
    path('todos-pets/', views.hotel_pets),
    path('', views.index),


]
