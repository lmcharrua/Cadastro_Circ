from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CreateCartasForm, CartaForm
from cmain.decorators import group_required 
import csv
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='userlogin')
@group_required(('TX', 'DAT'))
def editar_carta(request, pk):
    carta = Cartas.objects.get(id=pk)
    form = CartaForm(instance=carta)
    historico = hist_cartas.objects.filter(carta=carta).order_by('-data_alteracao')
    
    
    can_edit = request.user.has_perm('cartas.change_cartas' or 'cartas.add_cartas')
    
    if request.method == 'POST' and can_edit:
        form = CartaForm(request.POST, instance=carta)
        print(form.errors)
        if form.is_valid():
            form.instance._current_user = request.user.username  # pass user to signal
            form.save()
            return redirect('editar_carta', pk=carta.pk)
    return render(request, 'cartas/editar_carta.html', {'form': form, 'historico': historico, 'can_edit': can_edit})

@login_required(login_url='userlogin')
@group_required(('TX', 'DAT'))
def lista_cartas(request):
    cartas = Cartas.objects.exclude(estado="ABA").order_by('fabricante', 'part_number', 'serial_number')
    return render(request, 'cartas/lista_cartas.html', {'cartas': cartas})  

@login_required(login_url='userlogin')
@group_required(('TX', 'DAT'))
def criar_carta(request):
    can_edit = request.user.has_perm('cartas.change_cartas' or 'cartas.add_cartas')
    form = CreateCartasForm(request.POST)
    if form.is_valid():
        form.instance._current_user = request.user.username  # pass user to signal
        form.save()
        return redirect('editar_carta', pk=form.instance.id)
    context = {'form':form, 'can_edit': can_edit}
    return render(request, 'cartas/criar_carta.html', context=context)

@login_required(login_url='userlogin')
@group_required(('TX', 'DAT'))
def downloadc(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="cartas.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Fabricante', 'Data Receção', 'Tipo', 'Part Number', 'Serial Number', 'Descrição', 'Estado', 'Projeto', 'Sistema', 'Localização', 'Equipamento', 'Subrack', 'Slot', 'Porto', 'Observações'])

    cartas = Cartas.objects.all().values_list('fabricante', 'data_rececao', 'b_type', 'part_number', 'serial_number', 'descricao', 'estado', 'projeto', 'sistema', 'localizacao', 'equipamento', 'subrack', 'slot', 'porto', 'observacoes')
    for carta in cartas:
        writer.writerow(carta)

    return response