from django.db import models
from enum import Enum
from django_enum_choices.fields import EnumChoiceField


class Pessoa(models.Model):
    class Meta:
        abstract = True

    CPF = models.CharField(max_length=16, blank=False,null=False)
    nome = models.CharField(max_length=100,blank=False,null=False)

class Administrador(Pessoa):
    CTPS = models.CharField(max_length=25,blank=False,null=False)
    def __str__(self):
        return self.nome+" - Permissões de administrador"

class Monitor(Administrador):
    def __str__(self):
        return self.nome + " " + self.CTPS


class Cliente(Pessoa):
    email = models.EmailField(max_length=200,blank=True, null=False)
    tel = models.CharField(max_length=20, editable=True)

    def __str__(self):
        return self.nome


class Porte(Enum):
    Pequeno = 'P'
    Medio = 'M'
    Grande = 'G'


class Pet(models.Model):
    nome = models.CharField(max_length=30,blank=False,null=False)
    Porte = EnumChoiceField(Porte, blank=False)
    raca = models.CharField(max_length=50,blank=False)
    racao = models.CharField(max_length=30,blank=False, null=False)
    data_entrada = models.DateTimeField(verbose_name="Data de entrada",blank=False)
    dono = models.OneToOneField(Cliente, on_delete=models.CASCADE,blank=False)
    servicos = models.TextField(max_length=400,blank=True)

    def __str__(self):
        return "Pet: "+self.nome
