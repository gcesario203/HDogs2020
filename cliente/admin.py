from django.contrib import admin
from .models import Pet,Administrador,Cliente,Monitor

admin.site.register(Pet)
admin.site.register(Administrador)
admin.site.register(Cliente)
admin.site.register(Monitor)

class ListaPet(admin.ModelAdmin):
    list_display = ['nome' , 'dono', 'status']
# Register your models here.
