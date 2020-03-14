from django.contrib import admin
from .models import Pet

admin.site.register(Pet)

class ListaPet(admin.ModelAdmin):
    list_display = ['nome' , 'dono', 'status']
# Register your models here.
