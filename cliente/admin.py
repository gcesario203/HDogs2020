from django.contrib import admin
from .models import Pet,Administrador,Cliente,Monitor


class ListaPet(admin.ModelAdmin):
    list_display = ['_nome_pet','_tipo', 'dono']


class ListaCliente(admin.ModelAdmin):
    list_display = ['_nome' , '_email','_tel']


class ListaAdm(admin.ModelAdmin):
    list_display = ['_nome' , '_CTPS']

admin.site.register(Pet,ListaPet)
admin.site.register(Administrador,ListaAdm)
admin.site.register(Cliente,ListaCliente)
admin.site.register(Monitor,ListaAdm)
# Register your models here.
