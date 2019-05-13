from django.forms import ModelForm
from .models import Producao,Produto,Assinatura,Cooperativa,Endereco,Telefone
from django import forms

class FormCooperativa(forms.Form):
    razao_social=forms.CharField(label='Razão Social',max_length=100)
    nome_fantasia=forms.CharField(label='Nome Fantasia',max_length=100)
    logradouro=forms.CharField(label='Logradouro',max_length=80)
    numero=forms.IntegerField(label='Número')
    complemento=forms.CharField(label='Complemento',max_length=80)
    telefone=forms.CharField(label='Telefone',max_length=30)

class ModFormCooperativa(ModelForm):
    class Meta:
        model=Cooperativa
        fields=['razao_social','nome_fantasia','cnpj','email']

#Forms de Producao - INICIO
class FormProducao(forms.Form):
    produto=forms.ModelChoiceField(Produto.objects.all(),label='Produto',required=True)
    preco= forms.DecimalField(label='Preço',max_digits=3,decimal_places=2,required=True)
    quantidade=forms.DecimalField(label='Quantidade',max_digits=6,decimal_places=3,required=True)

class ModFormProducao(ModelForm):
    class Meta:
        model=Producao
        fields=['produto','preco','quantidade']

#Forms de Producao - FIM


#Forms de Assinatura - INICIO

class ModFormAssinatura(ModelForm):
    class Meta:
        model=Assinatura
        fields=['nome','preco','sazonalidade','tipo_pagamento','producoes']

    def __init__(self, cooperativa, *args, **kwargs):
        super(ModFormAssinatura, self).__init__(*args, **kwargs)
        self.fields['producoes'].queryset = Producao.objects.filter(cooperativa__id=cooperativa.id)

#Forms de Assinatura - FIM

#Forms de Endereco - INICIO

class ModFormEndereco(ModelForm):
    class Meta:
        model=Endereco
        fields=['logradouro','bairro','numero','complemento']

#Forms de Endereco - FIM

#Forms de telefone

class ModFormTelefone(ModelForm):
    class Meta:
        model=Telefone
        fields=['telefone']