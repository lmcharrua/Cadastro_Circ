from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import sdados, sterm
from .forms import StermForm, SdadosForm
from cmain.decorators import group_required 
from django.db.models import Q
from django.core.paginator import Paginator

@login_required(login_url='userlogin')
@group_required(('NOC', 'DADOS'))
def lista_sdados(request):
    pesquisar = request.POST.get('search', '')
    filtros = {
        "isid__icontains": request.POST.get('isid', ''),
        "isid_name__icontains": request.POST.get('isid_name', ''),
        "cliente__icontains": request.POST.get('cliente', ''),
        "estado__icontains": request.POST.get('estado', ''),
        "service_type__icontains": request.POST.get('service_type', ''),
        "created_at__icontains": request.POST.get('created_at', ''),
        }
    per_page = request.POST.get('per_page', 10 )
    sort = request.POST.get('sort', 'isid')
    direction = request.POST.get('direction', 'asc')

    l_sdados = sdados.objects.filter(
        Q(isid__icontains=pesquisar) |
        Q(isid_name__icontains=pesquisar) |
        Q(cliente__icontains=pesquisar) |
        Q(service_type__icontains=pesquisar) |
        Q(estado__icontains=pesquisar) |
        Q(created_at__icontains=pesquisar)
    )

    for field, value in filtros.items():
        if value:
            l_sdados = l_sdados.filter(**{field: value})

    if direction == 'desc':
        sort = '-' + sort
        l_sdados = l_sdados.order_by(sort)

    pages = Paginator(l_sdados, per_page)
    page_number = request.GET.get('page', 1)

    l_sdados = pages.get_page(page_number)

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=1)

    context = {
        'l_sdados': l_sdados,
        'per_page': per_page,
        'paginas': paginas,
        'sort': request.POST.get('sort', 'isid'),
        'direction': direction,
    }
    
    if request.htmx:
        return render(request, 'partials/tabela_sdados.html', context)

    return render(request, 'sdados/lista_sdados.html', context)

def criar_sdados(request, pk):
    pass

def editar_sdados(request, pk):
    pass

def editar_sterm(request, pk):
    pass

def criar_sterm(request, pk):
    pass



