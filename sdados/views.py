from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from .models import sdados, sterm
from .forms import sdadosForm, stermCreateForm, stermEditForm, stermForm

@login_required(login_url='userlogin')
def lista_sdados(request):
    lista = sdados.objects.exclude(Service_status="D").order_by('ISID')
    context = {
        'lista': lista
    }

    return render(request, 'lista_sdados.html', context=context)

@login_required(login_url='userlogin')
def detalhe_sdados(request, pk):
    servico = sdados.objects.get(id=pk)
    terminas = sterm.objects.all().filter(misid=pk).order_by('Local')
    context = {
        'servico': servico,
        'terminas': terminas,
    }
    return render(request, 'detalhe_sdados.html', context)

@login_required(login_url='userlogin')
def edit_sdados(request, pk):
    sd = sdados.objects.get(id=pk)
    form = sdadosForm(instance=sd)
    if request.method == 'POST':
        form = sdadosForm(request.POST, instance=sd)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponse("Serviço atualizado com sucesso!" )
    

    context = {
        'form': form,
        'servico': form    }
    return render(request, 'partials/form_det_serv.html', context=context)

@login_required(login_url='userlogin')
def edita_sterm(request,pk):
    termina = sterm.objects.get(id=pk)
    form = stermEditForm(instance=termina)
    if request.method == 'POST':
        form = stermEditForm(request.POST, instance=termina)
        if form.is_valid():
            form.save()
            return HttpResponse("Terminação atualizada com sucesso!" )
    context = {
        'form': form,
    }
    return render(request, 'partials/form_term.html', context=context)

@login_required(login_url='userlogin')
def criar_terminacao(request,pk):
    if request.method == 'GET':
        terminacao = stermCreateForm()
        teste = pk
        context = {
            'form': terminacao,
            'teste': teste
        }
        return render(request, 'partials/form_term.html', context=context)
    else:
        terminacao = stermCreateForm(request.POST)
        if terminacao.is_valid():
            terminacao.save()
            return HttpResponse("Terminação criada com sucesso!")
        else:
            print("Formulário inválido")
            print(terminacao.errors)

        context = {
            'form': terminacao,

        }
        return render(request, 'partials/form_term.html', context=context)
