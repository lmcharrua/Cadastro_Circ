from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import ServDadosForm, terminacaoForm, criarservdadosForm

@login_required(login_url='userlogin')
def lista_dados(request):
    l_dados = serv_dados.objects.exclude(Service_status='D')
    context = {'l_dados': l_dados}
    return render(request, 'dados/lista_dados.html', context=context)

@login_required(login_url='userlogin')
def editar_dados(request, pk):
    lisid = serv_dados.objects.get(id=pk)
    # term = serv_dados.terminacao_set.all()

    form = ServDadosForm(instance=lisid)
    if request.method == 'POST':
        form = ServDadosForm(request.POST, instance=lisid)

        if form.is_valid():
            form.save()
            print("gravado")
            return redirect('lista_dados')
        print(form.errors)

    context = {'form':form}
    return render(request, 'dados/editar_dados.html', context=context)

@login_required(login_url='userlogin')
def criar_dados(request):
    form = criarservdadosForm(request.POST)
    if form.is_valid():
        d=form.save()
        print (d.id)
        return redirect('editar_dados', pk=d.id)
    else:
        print(form.errors)
    context = {'form':form}
    return render(request, 'dados/criar_dados.html', context=context)

