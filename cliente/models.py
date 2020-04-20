from django.db import models
from enum import Enum
from django_enum_choices.fields import EnumChoiceField


class Pessoa(models.Model):
    _CPF = models.CharField(max_length=16, blank=False,null=False)
    _nome = models.CharField("Nome",max_length=100,blank=False,null=False)
    _email = models.EmailField("E-Mail",max_length=200,blank=True, null=False)
    _tel = models.CharField("Telefone",max_length=20,blank=True,null=True)


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


class Monitor(Administrador,Pessoa):
    
    class Meta:
        verbose_name = 'monitor'
        verbose_name_plural = 'monitores'

    def __str__(self):
        return self.nome + " - Carteira: " + self._CTPS


class Cliente(Pessoa):
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self._nome

class Porte(Enum):
    Pequeno = 'P'
    Medio = 'M'
    Grande = 'G'


class Pet(models.Model):
    _nome_pet = models.CharField("Nome do pet",max_length=30,blank=False,null=False)
    _tipo = models.CharField("Tipo",max_length=50,blank=False,null=False,default="Cachorro")
    _porte = EnumChoiceField(Porte, verbose_name="Porte",blank=False)
    _especie = models.CharField("Espécie:",max_length=50,blank=False,null=True)
    _racao = models.CharField("Ração",max_length=30,blank=False, null=False)
    data_entrada = models.DateTimeField(verbose_name="Data de entrada",blank=False)
    _dono = models.ForeignKey(Cliente, verbose_name="Dono",on_delete=models.CASCADE,blank=False)
    _servicos = models.TextField("Serviços",max_length=400,blank=True)

    class Meta:
        verbose_name = 'mascote'
        verbose_name_plural = 'mascotes'

    def __str__(self):
        return self._nome_pet+ " - Dono:"+self._dono._nome



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
        for code,label in Porte:
            if self._porte == code:
                break
        return label

    @porte.setter
    def porte(self,valor):
        if valor == 'p' or 'P':
            self._porte = Porte.Pequeno
        elif valor == 'm' or 'M':
            self._porte = Porte.Medio
        elif valor == 'g' or 'G':
            self._porte = Porte.Grande
        else:
            raise ValueError('Porte inválido, selecione entre pequeno(P ou p),médio(m ou M) ou grande(g ou G)')

    @property
    def dono(self):
        return self._dono.nome

    @dono.setter
    def dono(self,valor):
        if valor is Cliente:
            self._dono = valor
        else:
            raise ValueError('Cliente indisponível')

    @property
    def raca(self):
        return self._raca

    @raca.setter
    def raca(self,valor):
        self._raca = valor

    @property
    def racao(self):
        return self._racao

    @racao.setter
    def racao(self,valor):
        self._racao = valor

    @property
    def servicos(self):
        return self._servicos
    
    @servicos.setter
    def servicos(self,valor):
        self._servicos = valors