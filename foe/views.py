from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import circfoe
from .forms import circfoeForm, cria_circfoeForm
from cmain.decorators import group_required 


@login_required(login_url='userlogin')
@group_required(('NOC', 'FOE'))
def lista_foe(request):
    l_foe = circfoe.objects.exclude(estado='D')
    context = {'l_foe': l_foe}
    return render(request, 'foe/lista_foe.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE', 'NOC'))
def editar_foe(request, pk):
    lfoe = circfoe.objects.get(id=pk)
    net = request.GET.get('next')
    form = circfoeForm(instance=lfoe)
    can_edit = request.user.groups.filter(name='FOE').exists()
    if request.method == 'POST' and can_edit:
        form = circfoeForm(request.POST, instance=lfoe)
        if form.is_valid():
            form.save()
            return redirect(net)   
    context = {'form':form, 'can_edit': can_edit}
    return render(request, 'foe/editar_foe.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE', 'NOC'))
def criar_foe(request):
    form = cria_circfoeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_foe')
    context = {'form':form}
    return render(request, 'foe/criar_foe.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE',))
def desligados_foe(request):
    dlfoe = circfoe.objects.filter(estado='D')
    context = {'dlfoe': dlfoe}
    return render(request, 'foe/desligados_foe.html', context=context)