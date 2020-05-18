from django.db import models
from enum import Enum
from django_enum_choices.fields import EnumChoiceField
from django.contrib.auth.models import User


class Pessoa(models.Model):
    _CPF = models.CharField(max_length=16, blank=False,null=False, default=0)
    _nome = models.CharField("Nome",max_length=100,blank=False,null=False)
    _email = models.EmailField("E-Mail",max_length=200,blank=True, null=False, unique=True)
    _tel = models.CharField("Telefone",max_length=20,blank=True,null=True)
    user = models.OneToOneField(User, verbose_name="Usuario",on_delete=models.CASCADE, null=True)


    class Meta:
        abstract = True

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self,valor):
        self._nome = valor

    @property
    def CPF(self):
        return self._CPF

    @CPF.setter
    def CPF(self,valor):
        self._CPF = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self,valor):
        self._email = valor

    @property
    def tel(self):
        return self._tel

    @tel.setter
    def tel(self,valor):
        self._tel = valor

    def exibir_detalhes(self):
        dic = {}

        dic = {
            "nome":self.nome,
            "CPF":self.CPF,
            "email":self.email,
            "tel":self.tel
        }
        return dic


class Administrador(Pessoa):
    _CTPS = models.CharField(max_length=25,blank=False,null=False)

    class Meta:
        verbose_name = 'administrador'
        verbose_name_plural = 'administradores'

    def __str__(self):
        if self._nome:
            return self._nome+" - Permissões de administrador"
        return str(self.id)

    @property
    def CTPS(self):
        return self._CTPS
    
    @CTPS.setter
    def CTPS(self,valor):
        self._CTPS = valor

    def exibir_detalhes(self):
        dic = {}

        dic = {
            "nome":self.nome,
            "CTPS":self.CTPS,
            "email":self.email,
            "tel":self.tel
        }
        return dic


class Monitor(Pessoa):
    administrador = models.ForeignKey(Administrador, verbose_name="Administradores",on_delete=models.CASCADE, null=True,blank=True)
    _CTPS = models.CharField(max_length=25,blank=True,null=True)
    
    class Meta:
        verbose_name = 'monitor'
        verbose_name_plural = 'monitores'

    def __str__(self):
        return self.nome + " - Carteira: " + self._CTPS

    @property
    def CTPS(self):
        return self._CTPS
    
    @CTPS.setter
    def CTPS(self,valor):
        self._CTPS = valor

    def exibir_detalhes(self):
        dic = {}

        dic = {
            "nome":self.nome,
            "CTPS":self.CTPS,
            "email":self.email,
            "tel":self.tel
        }
        return dic


class Cliente(Pessoa):
    monitor_escolhido = models.ForeignKey(Monitor, verbose_name="Monitor responsável", on_delete=models.CASCADE, null=True,blank=True)
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self._nome


PEQUENO = 1
MEDIO = 2
GRANDE = 3

PORTE_MASCOTE = [
(1, 'Pequeno'),
(2, 'Médio'),
(3,'Grande')
]
class Pet(models.Model):
    _nome_pet = models.CharField("Nome do pet",max_length=30,blank=False,null=False)
    _tipo = models.CharField("Tipo",max_length=50,blank=False,null=False,default="Cachorro")
    _porte = models.PositiveIntegerField("porte do mascote",choices=PORTE_MASCOTE,default=PEQUENO)
    _especie = models.CharField("Espécie:",max_length=50,blank=False,null=True)
    _racao = models.CharField("Ração",max_length=30,blank=False, null=False)
    data_entrada = models.DateField(verbose_name="Data de entrada",auto_now_add=True)
    dono = models.ForeignKey(Cliente, verbose_name="Dono",on_delete=models.CASCADE,blank=False)

    class Meta:
        verbose_name = 'mascote'
        verbose_name_plural = 'mascotes'

    def __str__(self):
        return self.nome_pet+ " - Tipo: "+self.tipo+" - Espécie: "+self.especie

    @property
    def nome_pet(self):
        if self._nome_pet:
            return self._nome_pet
        return str(self.id)

    @nome_pet.setter
    def nome_pet(self,valor):
        self._nome_pet = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self,valor):
        self._tipo = valor

    @property
    def porte(self):
        for code,label in PORTE_MASCOTE:
            if self._porte == code:
                break
        return label

    @porte.setter
    def porte(self,valor):
        if valor == 'Pequeno':
            self._porte = PEQUENO
        elif valor == 'Medio':
            self._porte = MEDIO
        elif valor == 'Grande':
            self._porte = GRANDE
        else:
            raise ValueError('Porte inválido, selecione entre pequeno(P ou p),médio(m ou M) ou grande(g ou G)')

    @property
    def especie(self):
        return self._especie

    @especie.setter
    def especie(self,valor):
        self._especie = valor

    @property
    def racao(self):
        return self._racao

    @racao.setter
    def racao(self,valor):
        self._racao = valor

class Servicos(models.Model):
    _nome=models.CharField("Nome do serviço",max_length=300,blank=False,null=False,default="Nome do serviço prestado")
    _detalhes=models.TextField("Detalhes", max_length=1000,blank=False,null=False,default="Serviço prestado")
    data_criacao= models.DateField("Data de criação",auto_now_add=True)
    pet = models.ForeignKey(Pet,verbose_name="Pet que recebeu",on_delete=models.CASCADE, null=False,blank=False)
    monitor = models.ForeignKey(Monitor,verbose_name="Monitor que aplicou",on_delete=models.CASCADE, null=False,blank=False)

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'

    def __str__(self):
        return self.nome + " de "+self.pet.nome_pet

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self,valor):
        self._nome = valor

    @property
    def detalhes(self):
        return self._detalhes
    
    @detalhes.setter
    def detalhes(self,valor):
        self._detalhes = valor