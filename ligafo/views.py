from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import LigafoForm, criarligafoForm
from cmain.decorators import group_required 
from django.db.models import Q
from django.core.paginator import Paginator
from urllib.parse import parse_qs

# Create your views here.

@login_required(login_url='userlogin')
@group_required(('FOE', 'TX', 'DAT', 'DADOS', 'NOC'))
def editar_ligafo(request, pk):
    l = ligafo.objects.get(id=pk)
    net = request.GET.get('next')
    can_edit = request.user.has_perm('ligafo.change_ligafo' or 'ligafo.add_ligafo')

    form = LigafoForm(instance=l)
    if request.method == 'POST':
        form = LigafoForm(request.POST, instance=l)
        print(form)
        if form.is_valid():
            form.save()

            return redirect(net)   
    context = {'form':form , 'can_edit': can_edit}
    return render(request, 'ligafo/editar_ligafo.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE',))
def criar_ligafo(request):
    form = criarligafoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_ligafo')
    context = {'form':form}
    return render(request, 'ligafo/criar_ligafo.html', context=context)

@login_required(login_url='userlogin')
@group_required(('FOE',))
def desligados_ligafo(request):
    current_query = request.POST.urlencode()
    stored_query = request.session.get('ligafo_desligados_filters', '')

    if current_query:
        request.session['ligafo_desligados_filters'] = current_query
        querystring = current_query
        current_params = dict(request.POST.lists())
        filter_query = {k: v[0] if isinstance(v, list) and len(v) > 0 else v for k, v in current_params.items()}
    else:
        querystring = stored_query
        if stored_query:
            parsed = parse_qs(stored_query)
            filter_query = {k: v[0] if isinstance(v, list) and len(v) > 0 else v for k, v in parsed.items()}
        else:
            filter_query = {}

    pesquisar = filter_query.get('search', '')
    filtros = {
        "referencia__icontains": filter_query.get('referencia', ''),
        "cliente__icontains": filter_query.get('cliente', ''),
        "dist_optica__icontains": filter_query.get('dist_optica', ''),
        "dist_iet__icontains": filter_query.get('dist_iet', ''),
        "data_pedido__icontains": filter_query.get('data_pedido', ''),
        "data_entrega__icontains": filter_query.get('data_entrega', ''),
        "estado__exact": 'D',
        "local_a__icontains": filter_query.get('local_a', ''),
        "local_b__icontains": filter_query.get('local_b', ''),
        "observacoes__icontains": filter_query.get('observacoes', ''),
        }
    
    per_page = int(filter_query.get('per_page', 10))
    sort = filter_query.get('sort', 'referencia')
    direction = filter_query.get('direction', 'asc')
    

    lligafo = ligafo.objects.filter(
        Q(referencia__icontains=pesquisar) |
        Q(cliente__icontains=pesquisar) |
        Q(dist_optica__icontains=pesquisar) |
        Q(dist_iet__icontains=pesquisar) |
        Q(data_pedido__icontains=pesquisar) |
        Q(data_entrega__icontains=pesquisar) |
        Q(estado__icontains=pesquisar) |
        Q(local_a__icontains=pesquisar) |
        Q(local_b__icontains=pesquisar) |
        Q(observacoes__icontains=pesquisar)
    )

    for field, value in filtros.items():
        if value:
            lligafo = lligafo.filter(**{field: value})

    if direction == 'desc':
        sort = '-' + sort
    lligafo = lligafo.order_by(sort)

    pages = Paginator(lligafo, per_page)
    page_number = int(filter_query.get('page', request.POST.get('page', 1)))
 
    lligafo = pages.get_page(page_number)
   

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=1)

    context = {
        'lligafo': lligafo,
        'per_page': per_page,
        'paginas': paginas,
        'sort': sort,
        'direction': direction,
        'querystring': querystring,
        'filter_query': filter_query,
    }

    if request.htmx:
        return render(request, 'partials/tabela_dlfo.html', context=context)

    return render(request, 'ligafo/desligados_ligafo.html', context=context)

@login_required(login_url='userlogin')
@group_required(('NOC', 'FOE', 'TX', 'DAT', 'DADOS'))
def lista_ligafo(request):
    current_query = request.POST.urlencode()
    stored_query = request.session.get('ligafo_filters', '')

    if current_query:
        request.session['ligafo_filters'] = current_query
        querystring = current_query
        current_params = dict(request.POST.lists())
        filter_query = {k: v[0] if isinstance(v, list) and len(v) > 0 else v for k, v in current_params.items()}
    else:
        querystring = stored_query
        if stored_query:
            parsed = parse_qs(stored_query)
            filter_query = {k: v[0] if isinstance(v, list) and len(v) > 0 else v for k, v in parsed.items()}
        else:
            filter_query = {}

    pesquisar = filter_query.get('search', '')
    filtros = {
        "referencia__icontains": filter_query.get('referencia', ''),
        "cliente__icontains": filter_query.get('cliente', ''),
        "dist_optica__icontains": filter_query.get('dist_optica', ''),
        "dist_iet__icontains": filter_query.get('dist_iet', ''),
        "data_pedido__icontains": filter_query.get('data_pedido', ''),
        "data_entrega__icontains": filter_query.get('data_entrega', ''),
        "estado__icontains": filter_query.get('estado', ''),
        "local_a__icontains": filter_query.get('local_a', ''),
        "local_b__icontains": filter_query.get('local_b', ''),
        "observacoes__icontains": filter_query.get('observacoes', ''),
        }
    
    per_page = int(filter_query.get('per_page', 10))
    sort = filter_query.get('sort', 'referencia')
    direction = filter_query.get('direction', 'asc')
    

    lligafo = ligafo.objects.filter(
        Q(referencia__icontains=pesquisar) |
        Q(cliente__icontains=pesquisar) |
        Q(dist_optica__icontains=pesquisar) |
        Q(dist_iet__icontains=pesquisar) |
        Q(data_pedido__icontains=pesquisar) |
        Q(data_entrega__icontains=pesquisar) |
        Q(estado__icontains=pesquisar) |
        Q(local_a__icontains=pesquisar) |
        Q(local_b__icontains=pesquisar) |
        Q(observacoes__icontains=pesquisar)
    ).exclude(estado='D')

    for field, value in filtros.items():
        if value:
            lligafo = lligafo.filter(**{field: value})

    if direction == 'desc':
        sort = '-' + sort
    lligafo = lligafo.order_by(sort)

    pages = Paginator(lligafo, per_page)
    page_number = int(filter_query.get('page', request.POST.get('page', 1)))
 
    lligafo = pages.get_page(page_number)
   

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=1)

    context = {
        'lligafo': lligafo,
        'per_page': per_page,
        'paginas': paginas,
        'sort': sort,
        'direction': direction,
        'querystring': querystring,
        'filter_query': filter_query,
    }

    if request.htmx:
        return render(request, 'partials/tabela_lfo.html', context=context)

    return render(request, 'ligafo/lista_ligafo.html', context=context)