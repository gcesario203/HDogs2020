from django.db import models
from enum import Enum
from django_enum_choices.fields import EnumChoiceField
from django.contrib.auth.models import User


class Porte(Enum):
    Pequeno = 'P'
    Medio = 'M'
    Grande = 'G'


class Pet(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    data_de_nascimento = models.DateField(blank=False)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    porte = EnumChoiceField(Porte, blank=False)
    notas = models.TextField(blank=True)

    def __str__(self):
        return self.nome
