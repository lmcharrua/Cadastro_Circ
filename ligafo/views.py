from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import LigafoForm, criarligafoForm


# Create your views here.

@login_required(login_url='userlogin')
def lista_ligafo(request):
    l_ligafo = ligafo.objects.exclude(estado='D')
    context = {'ligafos': l_ligafo}
    return render(request, 'ligafo/lista_ligafo.html', context=context)

@login_required(login_url='userlogin')
def editar_ligafo(request, pk):
    l = ligafo.objects.get(id=pk)
    net = request.GET.get('next')

    form = LigafoForm(instance=l)
    if request.method == 'POST':
        form = LigafoForm(request.POST, instance=l)

        if form.is_valid():
            form.save()

            return redirect(net)   
    context = {'form':form}
    return render(request, 'ligafo/editar_ligafo.html', context=context)

@login_required(login_url='userlogin')
def criar_ligafo(request):
    form = criarligafoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_ligafo')
    context = {'form':form}
    return render(request, 'ligafo/criar_ligafo.html', context=context)

@login_required(login_url='userlogin')
def desligados_ligafo(request):
    desligados_ligafo = ligafo.objects.filter(estado='D')
    context = {'dligafos': desligados_ligafo}
    return render(request, 'ligafo/desligados_ligafo.html', context=context)
