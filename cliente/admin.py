from django.contrib import admin
from .models import Pet,Administrador,Cliente,Monitor,Servicos


class ListaPet(admin.ModelAdmin):
    list_display = ['_nome_pet','_tipo', 'dono']


class ListaCliente(admin.ModelAdmin):
    list_display = ['_nome' , '_email','_tel','user']


class ListaAdm(admin.ModelAdmin):
    list_display = ['_nome' , '_CTPS']

class ListaServicos(admin.ModelAdmin):
    list_display = ['nome','pet','monitor','data']

admin.site.register(Pet,ListaPet)
admin.site.register(Administrador,ListaAdm)
admin.site.register(Cliente,ListaCliente)
admin.site.register(Monitor,ListaAdm)
admin.site.register(Servicos,ListaServicos)
# Register your models here.
