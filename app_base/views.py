from django.shortcuts import render,redirect, get_object_or_404
from .models import Endereco,Cooperativa,Producao,Produto,Assinatura
from . import forms
from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request,'index.html')

def my_logout(request):
    logout(request)
    return redirect('login')

#Views de cooperativa - INICIO
def cooperativa_create(request):
    form= forms.FormCooperativa(request.POST or None)

    if form.is_valid():
        endereco= Endereco(
            logradouro=form.cleaned_data['logradouro'],
            numero=form.cleaned_data['numero'],
            complemento=form.cleaned_data['complemento'],
            telefone=form.cleaned_data['telefone']
        )
        endereco.save()
        #enderecoR=endereco.refresh_from_db()
        cooperativa= Cooperativa(
            usuario=request.user,
            razao_social=form.cleaned_data['razao_social'],
            nome_fantasia=form.cleaned_data['nome_fantasia'],
            aprovado=False,
            endereco=endereco
        )
        cooperativa.save()
        return redirect('login/')
    return render(request, 'cooperativa/form_cadastro.html', {'form': form})

def cooperativa_view(request):
    cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
    return render(request, 'cooperativa/view.html', {'cooperativa': cooperativa})

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
    form = forms.FormProducao(request.POST or None)
    acao='Cadastrar'
    if form.is_valid():
        cooperativa = Cooperativa.objects.filter(usuario__id=request.user.id).first()
        #cooperativa= Cooperativa.objects.select_related('usuario').get(id=request.user.id)
        producao=Producao(quantidade=form.cleaned_data['quantidade'],preco=form.cleaned_data['preco'],produto=form.cleaned_data['produto'],cooperativa=cooperativa)
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
    return render(request, 'assinatura/form_cadastro.html', {'form': form, 'acao': acao})

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
    return render(request, 'assinatura/form_cadastro.html', {'form': form, 'acao': acao})

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