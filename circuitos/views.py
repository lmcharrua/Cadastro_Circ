from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CircuitoForm, CreateCircuitoForm
from cmain.decorators import group_required 


@login_required(login_url='userlogin')
@group_required(('NOC', 'TX', 'DAT', 'DADOS', 'VOZ'))
def lista_cct(request):
    l_circuitos= Circuitos.objects.exclude(Estado_Cct="Desligado")
    context = {'circuitos': l_circuitos}

    return render(request, 'circuitos/lista_circuitos.html', context=context)

@login_required(login_url='userlogin')
@group_required(('NOC', 'TX', 'DAT', 'DADOS', 'VOZ'))
def ver_circuito(request, pk):
    all_circuitos = Circuitos.objects.get(id=pk)
    context = {'circuito':all_circuitos}
    return render(request, 'circuitos/ver_circuito.html', context=context)

@login_required(login_url='userlogin')
@group_required(('NOC','TX', 'DAT', 'DADOS', 'VOZ'))
def editar_circuito(request, pk):
    cct = Circuitos.objects.get(id=pk)
    form = CircuitoForm(instance=cct)
    can_edit = request.user.has_perm('circuitos.change_circuitos' or 'circuitos.add_circuitos')

    if request.method == 'POST' and can_edit:
        form = CircuitoForm(request.POST,instance=cct)
        if form.is_valid():
            form.save()
            messages.success(request, "O circuito foi actualizado com sucesso!")
            print("Circuito actualizado")
            return redirect("lista_cct")   
    context = {'form':form, 'can_edit': can_edit}
    return render(request, 'circuitos/editar_circuito.html', context=context)

@login_required(login_url='userlogin')
@group_required(('TX', 'DAT', 'DADOS'))
def criar_circuito(request):
    form = CreateCircuitoForm(request.POST)
    if form.is_valid():
        form.save()
        # messages.success(request, "O circuito foi criado com sucesso!")
        return redirect('lista_cct')
    context = {'form':form}
    return render(request, 'circuitos/criar_circuito.html', context=context)
