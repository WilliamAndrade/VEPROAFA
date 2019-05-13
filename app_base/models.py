from django.conf import settings
from django.db import models

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=80)
    tipo = models.CharField(max_length=25)
    un_medida = models.CharField(max_length=2)
    foto = models.ImageField(upload_to='img_produtos', null=True, blank=True)

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    logradouro = models.CharField(max_length=130)
    bairro=models.CharField(max_length=80)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=80)

    def __str__(self):
        return self.logradouro

'''
    A data de pagamento foi retirada da tabela de tipo de pagamento
    devido a este atributo estar mais relacionado com a tabela de 
    assinatura ja que a mesma ja possui o atributo sazonalidade
'''
class TipoPagamento(models.Model):
    tipo = models.CharField(max_length=45)

    def __str__(self):
        return self.tipo

class Producao(models.Model):
    cooperativa= models.ForeignKey('Cooperativa',null=False,blank=False,on_delete= models.PROTECT)
    produto=models.ForeignKey(Produto,null=False,blank=False,on_delete= models.PROTECT)
    preco=models.DecimalField(max_digits=3,decimal_places=2)
    quantidade= models.DecimalField(decimal_places=3, max_digits=6)

    def __str__(self):
        return 'Produção de '+self.produto.nome


class Assinatura(models.Model):
    nome = models.CharField(max_length=120,default='')
    preco = models.DecimalField(max_digits=6,decimal_places=3)
    sazonalidade = models.CharField(max_length=45)
    tipo_pagamento= models.ManyToManyField(TipoPagamento,blank=False)
    producoes= models.ManyToManyField(Producao,blank=False)

    def __str__(self):
        return self.nome

class Cooperativa(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,blank=True,null=True)
    razao_social=models.CharField(max_length=100)
    nome_fantasia=models.CharField(max_length=100)
    cnpj=models.CharField(max_length=20)
    email= models.EmailField()
    aprovado=models.NullBooleanField()
    endereco = models.OneToOneField(Endereco, null=False, blank=False, on_delete=models.CASCADE)
    assinaturas= models.ManyToManyField(Assinatura, blank=True)

    def __str__(self):
        return self.nome_fantasia


class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    nome=models.CharField(max_length=100)
    cpf_cnpj=models.CharField(max_length=25)
    email= models.EmailField()
    endereco= models.OneToOneField(Endereco, null=False, blank=False, on_delete=models.CASCADE)
    assinaturas= models.ManyToManyField(Assinatura,blank=False)

    def __str__(self):
        return self.nome


class Telefone(models.Model):
    telefone = models.CharField(max_length=30)
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE,null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.cooperativa.nome_fantasia + ' '+self.telefone