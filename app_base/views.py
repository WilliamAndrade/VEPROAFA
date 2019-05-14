from django.shortcuts import render,redirect, get_object_or_404
from .models import Endereco,Cooperativa,Producao,Produto,Assinatura,Telefone,Cliente
from . import forms
from django.contrib.auth import logout
import json

# Create your views here.

def index(request):
    return render(request,'index.html')

def my_logout(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    producoes = Producao.objects.filter(cooperativa=cooperativa)

    nomes=[producao.produto.nome for producao in producoes]
    valores=[int(producao.preco) for producao in producoes]

    context={
        'nomes':json.dumps(nomes),
        'valores':json.dumps(valores)
    }

    return render(request,'dashboard/dashboard.html',context)

#Views de cooperativa - INICIO
def cooperativa_create(request):
    formCooperativa= forms.ModFormCooperativa(request.POST or None)
    formTelefone=forms.ModFormTelefone(request.POST or None)
    formEndereco=forms.ModFormEndereco(request.POST or None)

    if formCooperativa.is_valid() and formEndereco.is_valid() and formTelefone.is_valid():
        cooperativa=formCooperativa.save(commit=False)
        cooperativa.endereco=formEndereco.save()
        telefone=formTelefone.save(commit=False)
        telefone.cooperativa=cooperativa.save()
        telefone.save()
        return redirect('login/')
    return render(request, 'cooperativa/form_cadastro.html', {'formCooperativa': formCooperativa,'formTelefone':formTelefone,'formEndereco':formEndereco})

def cooperativa_view(request):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    telefones=Telefone.objects.filter(cooperativa=cooperativa)
    return render(request, 'cooperativa/view.html', {'cooperativa': cooperativa,'telefones':telefones})

def cooperativa_update(request,id):
    cooperativa = get_object_or_404(Cooperativa, pk=id)
    form = forms.ModFormCooperativa(request.POST or None, instance=cooperativa)

    if form.is_valid():
        form.save()
        return redirect('cooperativa_view')
    return render(request, 'cooperativa/form.html', {'form': form})

#Views de cooperativa - FIM

#Views de Producao - INICO

def producao_create(request):
    form = forms.ModFormProducao(request.POST or None)
    acao='Cadastrar'
    if form.is_valid():
        cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
        #cooperativa= Cooperativa.objects.select_related('usuario').get(id=request.user.id)
        producao=form.save(commit=False)
        producao.cooperativa=cooperativa
        producao.save()
        return redirect('producao_list')
    return render(request, 'producao/form.html', {'form': form,'acao':acao})

def producao_list(request):
    cooperativa=Cooperativa.objects.filter(usuario__id=request.user.id).first()
    producoes=Producao.objects.filter(cooperativa=cooperativa)

    return render(request,'producao/list.html',{'producoes':producoes})

def producao_update(request, id):
    producao= get_object_or_404(Producao, pk=id)
    form=forms.ModFormProducao(request.POST or None, instance=producao)
    acao='Atualizar'

    if form.is_valid():
        form.save()
        return redirect('producao_list')
    return render(request,'producao/form.html',{'form': form,'acao':acao})

def producao_delete(request, id):
    producao = get_object_or_404(Producao, pk=id)
    form = forms.ModFormProducao(request.POST or None, instance=producao)

    if request.method == 'POST':
        producao.delete()
        return redirect('producao_list')
    return render(request,'producao/delete.html',{'form':form})

#Views de Producao - FIM


#Views de Produto - INICIO

def produto_list(request):
    produtos=Produto.objects.all()
    return render(request, 'produto/list.html', {'produtos': produtos})

def produto_view(request, id):
    produto= get_object_or_404(Produto, pk=id)
    return render(request, 'produto/view.html', {'produto': produto})

#Views de Produto - FIM


#Views de Assinatura - INICIO

def assinatura_create(request):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    form = forms.ModFormAssinatura(cooperativa,request.POST or None)
    acao = 'Cadastrar'
    if form.is_valid():
        assinatura=form.save(commit=True)
        cooperativa.refresh_from_db()
        cooperativa.assinaturas.add(assinatura)
        return redirect('assinatura_list')
    return render(request, 'assinatura/form.html', {'form': form, 'acao': acao})

def assinatura_list(request):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    assinaturas= cooperativa.assinaturas.all()
    return render(request, 'assinatura/list.html', {'assinaturas': assinaturas})

def assinatura_update(request, id):
    assinatura = get_object_or_404(Assinatura, pk=id)
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()

    form = forms.ModFormAssinatura(cooperativa,request.POST or None, instance=assinatura)
    acao = 'Atualizar'

    if form.is_valid():
        form.save()
        return redirect('assinatura_list')
    return render(request, 'assinatura/form.html', {'form': form, 'acao': acao})

def assinatura_delete(request, id):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    assinatura = get_object_or_404(Assinatura, pk=id)

    form = forms.ModFormAssinatura(cooperativa,request.POST or None, instance=assinatura)

    if request.method == 'POST':
        assinatura.delete()
        return redirect('assinatura_list')
    return render(request, 'assinatura/delete.html', {'form': form})

#Views de Assinatura - FIM

#Views de Endereco - INICIO

def endereco_update(request,id):
    endereco = get_object_or_404(Endereco, pk=id)
    form = forms.ModFormEndereco(request.POST or None, instance=endereco)

    if form.is_valid():
        form.save()
        return redirect('cooperativa_view')
    return render(request, 'endereco/form.html', {'form': form})

#Views de Endereco - FIM

#Views de Telefone

def telefone_create(request, id):
    form=forms.ModFormTelefone(request.POST or None)
    acao='Cadastrar'

    if form.is_valid():
        cooperativa = get_object_or_404(Cooperativa, pk=id)
        telefone=form.save(commit=False)
        telefone.cooperativa=cooperativa
        telefone.save()
        return redirect('cooperativa_view')
    return render(request, 'telefone/form.html', {'form': form, 'acao':acao})

def telefone_update(request, id):
    telefone = get_object_or_404(Telefone, pk=id)
    form = forms.ModFormProducao(request.POST or None, instance=telefone)
    acao = 'Atualizar'

    if form.is_valid():
        form.save()
        return redirect('cooperativa_view')
    return render(request, 'telefone/form.html', {'form': form, 'acao': acao})

def telefone_delete(request, id):
    telefone = get_object_or_404(Telefone, pk=id)
    form = forms.ModFormTelefone(request.POST or None, instance=telefone)

    if request.method == 'POST':
        telefone.delete()
        return redirect('cooperativa_view')
    return render(request, 'telefone/delete.html', {'form': form})

#VIEWS Assinaturas
def list_all(request):
    ass = Assinatura.objects.get(pk=request.user.id)
    cliente = Cliente.objects.filter(assinaturas=ass.id).select_related()
    assinatura = cliente.assinaturas.all()
    #ativo = Cliente.objects.filter(user=request.user.id)
    title = "Assinaturas"
    return render(request,"assinatura/list_all.html",{"title":title,"cliente":cliente,"assinatura":assinatura})

def assinar(request,id):
    cli = get_object_or_404(Cliente,pk=id)

    form = forms.FormAssinatura(request.POST or None, instance=cli)
    if form.is_valid():
        form.save()
        return redirect('list_all')
    return render(request,'assinatura/assinar.html',{"form":form})

