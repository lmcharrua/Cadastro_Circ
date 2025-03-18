from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import circfoe
from .forms import circfoeForm, cria_circfoeForm


# Create your views here.

@login_required(login_url='userlogin')
def lista_foe(request):
    l_foe = circfoe.objects.exclude(estado='D')
    context = {'l_foe': l_foe}
    return render(request, 'ligafo/lista_foe.html', context=context)

@login_required(login_url='userlogin')
def editar_foe(request, pk):
    lfoe = circfoe.objects.get(id=pk)
    net = request.GET.get('next')

    form = circfoeForm(instance=lfoe)
    if request.method == 'POST':
        form = circfoeForm(request.POST, instance=lfoe)

        if form.is_valid():
            form.save()

            return redirect(net)   
    context = {'form':form}
    return render(request, 'ligafo/editar_foe.html', context=context)

@login_required(login_url='userlogin')
def criar_foe(request):
    form = cria_circfoeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_foe')
    context = {'form':form}
    return render(request, 'ligafo/criar_foe.html', context=context)

@login_required(login_url='userlogin')
def desligados_foe(request):
    desligados_foe = circfoe.objects.filter(estado='D')
    context = {'dlfoe': desligados_foe}
    return render(request, 'ligafo/desligados_foe.html', context=context)