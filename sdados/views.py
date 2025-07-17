""" from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from .models import sdados, sterm
from .forms import *

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
    if request.method == 'GET':
        sd = get_object_or_404(sdados, id=pk)
        form = sdadosForm(instance=sd)
        context = {
            'form': form,
        }
        return render(request, 'partials/form_det_serv.html', context=context)
    sd = sdados.objects.get(id=pk)
    form = sdadosForm(instance=sd)
    if request.method == 'POST':
        form = sdadosForm(request.POST, instance=sd)
        if form.is_valid():
            form.save()
            return HttpResponse("Serviço atualizado com sucesso!")
     context = {
        'form': form,
    }
    return render(request, 'partials/form_det_serv.html', context) 

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
  
        context = {
            'form': terminacao,

        }
        return render(request, 'partials/form_term.html', context=context)
    
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

 """

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .models import sdados, sterm
from .forms import StermForm, SdadosForm

def sdados_list(request):
    records = sdados.objects.exclude(Service_status='D')
    return render(request, 'app/sdados_list.html', {'records': records})

def sdados_disabled(request):
    records = sdados.objects.filter(Service_status='D')
    return render(request, 'app/sdados_disabled.html', {'records': records})

def sdados_detail(request, pk):
    record = get_object_or_404(sdados, pk=pk)
    terms = sterm.objects.filter(misid=record)
    return render(request, 'app/sdados_detail.html', {'record': record, 'terms': terms})

def sterm_create(request, pk):
    record = get_object_or_404(sdados, pk=pk)
    if request.method == 'POST':
        form = StermForm(request.POST)
        if form.is_valid():
            sterm_instance = form.save(commit=False)
            sterm_instance.misid = record
            sterm_instance.save()
            terms = sterm.objects.filter(misid=record)
            html = render_to_string('app/partials/sterm_table.html', {'terms': terms, 'record': record})
            response = HttpResponse(html)
            response['HX-Trigger'] = 'closeModal'
            return response
    else:
        form = StermForm()
    return render(request, 'app/forms/sterm_form.html', {'form': form, 'record': record})

def sterm_edit(request, pk):
    term = get_object_or_404(sterm, pk=pk)
    record = term.misid
    if request.method == 'POST':
        form = StermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            terms = sterm.objects.filter(misid=record)
            html = render_to_string('app/partials/sterm_table.html', {'terms': terms, 'record': record})
            response = HttpResponse(html)
            response['HX-Trigger'] = 'closeModal'
            return response
    else:
        form = StermForm(instance=term)
    return render(request, 'app/forms/sterm_edit_form.html', {'form': form, 'record': record, 'term': term})

def sdados_edit(request, pk):
    record = get_object_or_404(sdados, pk=pk)
    if request.method == 'POST':
        form = SdadosForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'closeModal'})
    else:
        form = SdadosForm(instance=record)
    return render(request, 'app/forms/sdados_form.html', {'form': form})

@require_POST
def sdados_disable(request, pk):
    record = get_object_or_404(sdados, pk=pk)
    record.Service_status = 'D'
    record.save()
    return HttpResponse(status=204)

@require_POST
def sdados_reactivate(request, pk):
    record = get_object_or_404(sdados, pk=pk)
    record.Service_status = ''
    record.save()
    return HttpResponse(status=204)