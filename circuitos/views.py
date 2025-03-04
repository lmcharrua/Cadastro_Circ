from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import UpdateCircuitoForm, CreateCircuitoForm

@login_required(login_url='userlogin')
def lista_cct(request):
    l_circuitos= Circuitos.objects.exclude(Estado_Cct="Desligado")
    context = {'circuitos': l_circuitos}

    return render(request, 'circuitos/lista_circuitos.html', context=context)

@login_required(login_url='userlogin')
def ver_circuito(request, pk):
    all_circuitos = Circuitos.objects.get(id=pk)
    context = {'circuito':all_circuitos}
    return render(request, 'circuitos/ver_circuito.html', context=context)

@login_required(login_url='userlogin')
def editar_circuito(request, pk):
    circuito = Circuitos.objects.get(id=pk)
    form = UpdateCircuitoForm(instance=circuito)
    if request.method == 'POST':
        form = UpdateCircuitoForm(request.POST, instance=circuito)
        if form.is_valid():
            form.save()
            messages.success(request, "O circuito foi actualizado com sucesso!")
            return redirect("main")   
    context = {'form':form}
    return render(request, 'circuitos/editar_circuito.html', context=context)


