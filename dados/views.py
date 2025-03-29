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
    context = {'ldados': l_dados}
    return render(request, 'dados/lista_dados.html', context=context)

@login_required(login_url='userlogin')
def editar_dados(request, pk):
    l = serv_dados.objects.get(id=pk)
    term = serv_dados.terminacao_set.all()
    net = request.GET.get('next')

    form = ServDadosForm(instance=l)
    if request.method == 'POST':
        form = ServDadosForm(request.POST, instance=l)

        if form.is_valid():
            form.save()

            return redirect(net)   
    context = {'form':form}
    return render(request, 'dados/editar_dados.html', context=context)

@login_required(login_url='userlogin')
def criar_dados(request):
    form = criarservdadosForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_dados')
    context = {'form':form}
    return render(request, 'dados/criar_dados.html', context=context)

