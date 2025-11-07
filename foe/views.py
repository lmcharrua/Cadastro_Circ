from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import circfoe
from .forms import circfoeForm, cria_circfoeForm
from cmain.decorators import group_required 
from django.db.models import Q
from django.core.paginator import Paginator

@login_required(login_url='userlogin')
@group_required(('FOE', 'NOC'))
def editar_foe(request, pk):
    lfoe = circfoe.objects.get(id=pk)
    net = request.GET.get('next')
    form = circfoeForm(instance=lfoe)
    criado = form.instance.created_at.strftime('%d-%b-%Y')
    editado = form.instance.updated_at.strftime('%d-%b-%Y')
    can_edit = request.user.groups.filter(name='FOE').exists()
    if request.method == 'POST' and can_edit:
        form = circfoeForm(request.POST, instance=lfoe)
        if form.is_valid():
            form.instance.update_user = request.user.username
            form.save()
            return redirect(net)   
    context = {'form':form, 'can_edit': can_edit, 'criado': criado, 'editado': editado}
    return render(request, 'foe/editar_foe.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE',))
def criar_foe(request):
    form = cria_circfoeForm(request.POST)
    if form.is_valid():
        form.save()
        form.instance.create_user = request.user.username
        return redirect('editar_foe', pk=form.instance.id)
    context = {'form':form}
    return render(request, 'foe/criar_foe.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE',))
def desligados_foe(request):
    pesquisar = request.POST.get('search', '')
    filtros = {
        "referencia__icontains": request.POST.get('referencia', ''),
        "encomenda__icontains": request.POST.get('encomenda', ''),
        "cliente__icontains": request.POST.get('cliente', ''),
        "estado__exact": 'D',
        "tipo_ocupa__icontains": request.POST.get('tipo_ocupa', ''),
        "data_obj__icontains": request.POST.get('data_obj', ''),
        "data_entrega__icontains": request.POST.get('data_entrega', ''),
        "dist_km__icontains": request.POST.get('dist_km', ''),
        "dist_optica__icontains": request.POST.get('dist_optica', ''),
        "local_a__icontains": request.POST.get('local_a', ''),
        "local_b__icontains": request.POST.get('local_b', ''),
        }
    
    per_page = request.POST.get('per_page', 10)
    sort = request.POST.get('sort', 'referencia')
    direction = request.POST.get('direction', 'asc')

    lfoes = circfoe.objects.filter(
        Q(referencia__icontains=pesquisar) |
        Q(encomenda__icontains=pesquisar) |
        Q(cliente__icontains=pesquisar) |
        Q(estado__icontains=pesquisar) |
        Q(tipo_ocupa__icontains=pesquisar) |
        Q(data_obj__icontains=pesquisar) |
        Q(data_entrega__icontains=pesquisar) |
        Q(dist_km__icontains=pesquisar) |
        Q(dist_optica__icontains=pesquisar) |
        Q(local_a__icontains=pesquisar) |
        Q(local_b__icontains=pesquisar)
    )
    for field, value in filtros.items():
        if value:
            lfoes = lfoes.filter(**{field: value})

    if direction == 'desc':
        sort = f"-{sort}"
    lfoes = lfoes.order_by(sort)

    pages = Paginator(lfoes, per_page)
    page_number = request.POST.get('page', 1)

    lfoes = pages.get_page(page_number)

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=2)
    context = {
        'foes': lfoes,
        'per_page': per_page,
        'paginas': paginas,
        "sort": request.POST.get("sort", ""),
        "direction": direction,
    }

    if request.htmx:
        return render(request, 'partials/tabela_dfoe.html', context=context)
    return render(request, 'foe/desligados_foe.html', context)


@login_required(login_url='userlogin')
@group_required(('NOC', 'FOE'))
def lista_foe(request):
    pesquisar = request.POST.get('search', '')
    filtros = {
        "referencia__icontains": request.POST.get('referencia', ''),
        "encomenda__icontains": request.POST.get('encomenda', ''),
        "cliente__icontains": request.POST.get('cliente', ''),
        "estado__icontains": request.POST.get('estado', ''),
        "tipo_ocupa__icontains": request.POST.get('tipo_ocupa', ''),
        "data_obj__icontains": request.POST.get('data_obj', ''),
        "data_entrega__icontains": request.POST.get('data_entrega', ''),
        "dist_km__icontains": request.POST.get('dist_km', ''),
        "dist_optica__icontains": request.POST.get('dist_optica', ''),
        "local_a__icontains": request.POST.get('local_a', ''),
        "local_b__icontains": request.POST.get('local_b', ''),
        }
    
    per_page = request.POST.get('per_page', 10)
    sort = request.POST.get('sort', 'referencia')
    direction = request.POST.get('direction', 'asc')

    lfoes = circfoe.objects.filter(
        Q(referencia__icontains=pesquisar) |
        Q(encomenda__icontains=pesquisar) |
        Q(cliente__icontains=pesquisar) |
        Q(estado__icontains=pesquisar) |
        Q(tipo_ocupa__icontains=pesquisar) |
        Q(data_obj__icontains=pesquisar) |
        Q(data_entrega__icontains=pesquisar) |
        Q(dist_km__icontains=pesquisar) |
        Q(dist_optica__icontains=pesquisar) |
        Q(local_a__icontains=pesquisar) |
        Q(local_b__icontains=pesquisar)
    ).exclude(estado='D')

    for field, value in filtros.items():
        if value:
            lfoes = lfoes.filter(**{field: value})

    if direction == 'desc':
        sort = f"-{sort}"
    lfoes = lfoes.order_by(sort)

    pages = Paginator(lfoes, per_page)
    page_number = request.POST.get('page', 1)

    lfoes = pages.get_page(page_number)

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=2)
    context = {
        'foes': lfoes,
        'per_page': per_page,
        'paginas': paginas,
        "sort": request.POST.get("sort", ""),
        "direction": direction,
    }

    if request.htmx:
        return render(request, 'partials/tabela_foe.html', context=context)
    return render(request, 'foe/lista_foe.html', context)
