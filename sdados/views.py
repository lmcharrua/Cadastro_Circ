from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
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

@login_required(login_url='userlogin')
@group_required(('DADOS', ))
def criar_sdados(request):
    form = SdadosForm(request.POST)
    print(request.POST)
    print(form.errors)
    if form.is_valid():
        form.save()
        print('Serviço criado com sucesso.')
        return redirect('editar_sdados', pk=form.instance.id)
    context = {'form': form} 
    return render(request, 'sdados/criar_sdados.html', context)

@login_required(login_url='userlogin')
@group_required(('DADOS',))
def editar_sdados(request, pk):
    sd = sdados.objects.get(id=pk)
    terminas = sterm.objects.filter(misid=sd.isid)
    can_edit = request.user.has_perm('sdados.change_sdados' or 'sdados.add_sdados')
    form = SdadosForm(instance=sd)
    if request.method == 'POST':
        #print(request.POST)
        form = SdadosForm(request.POST, instance=sd)
        if form.is_valid():
            print("passou o teste")
            print(form.errors)
            
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso.')
            context = {'form': form,'can_edit': can_edit, 'terminas': terminas} 
            print (form)
            #return redirect('editar_sdados', pk=form.instance.id)
            return render(request, 'sdados/editar_sdados.html', context)
    print(form)
    context = {'form': form,'can_edit': can_edit, 'terminas': terminas} 
    return render(request, 'sdados/editar_sdados.html', context)


@login_required(login_url='userlogin')
@group_required(('DADOS',))
def editar_sterm(request, pk):
    form = StermForm()
    form.fields['misid'].initial = pk
    if request.method == 'POST':
        form = StermForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terminal adicionado com sucesso.')
            return redirect('editar_sdados', pk=pk)
    context = {'form': form} 
    return render(request, 'partials/editar_sterm.html', context)



@login_required(login_url='userlogin')
@group_required(('DADOS',))
def criar_sterm(request):
    misid = request.GET.get('misid')
    form = StermForm()
    form.fields['misid'].initial = misid
    if request.method == 'POST':
        misid = request.POST.get('misid')
        form = StermForm(request.POST)
        if form.is_valid():
            form.save()
            smisid = form.instance.misid
            sd = sdados.objects.get(id=smisid)
            terminas = sterm.objects.filter(misid=sd.isid)
            can_edit = request.user.has_perm('sdados.change_sdados' or 'sdados.add_sdados')
            form = SdadosForm(instance=sd)
            context = {'form': form,'can_edit': can_edit, 'terminas': terminas} 
            messages.success(request, 'Terminal adicionado com sucesso.')
            #return render(request, 'sdados/editar_sdados.html', context)
            return render(request, 'partials/form_edit_sdados.html', context)
    context = {'form': form, 'serv': misid} 
    return render(request, 'partials/criar_sterm.html', context)


# Segunda versão do módulo de dados 

@login_required(login_url='userlogin')
@group_required(('NOC', 'DADOS'))
def lsdados(request):
    pesquisar = request.GET.get('search', '')
    filtros = {
        "isid__icontains": request.GET.get('isid', ''),
        "isid_name__icontains": request.GET.get('isid_name', ''),
        "cliente__icontains": request.GET.get('cliente', ''),
        "estado__icontains": request.GET.get('estado', ''),
        "service_type__icontains": request.GET.get('service_type', ''),
        "created_at__icontains": request.GET.get('created_at', ''),
        }
    per_page = request.GET.get('per_page', 10 )
    sort = request.GET.get('sort', 'isid')
    direction = request.GET.get('direction', 'asc')

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
    print (page_number)

    l_sdados = pages.get_page(page_number)

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=1)

    context = {
        'l_sdados': l_sdados,
        'per_page': per_page,
        'paginas': paginas,
        'sort': request.GET.get('sort', 'isid'),
        'direction': direction,
        'querystring': request.GET.urlencode(),  # useful for pagination links
    }
    
    if request.htmx:
        return render(request, 'partials/tsdados.html', context)

    return render(request, 'sdados/lsdados.html', context)

@login_required(login_url='userlogin')
@group_required(('DADOS',))
def esdados(request, pk):
    sd = sdados.objects.get(id=pk)
    terminas = sterm.objects.filter(misid=sd.isid)
    can_edit = request.user.has_perm('sdados.change_sdados' or 'sdados.add_sdados')
    form = SdadosForm(instance=sd)
    back_to_list = request.GET.urlencode()
    if request.method == 'POST':
        #print(request.POST)
        form = SdadosForm(request.POST, instance=sd)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso.')
            return redirect(request.path + f"?{back_to_list}")
            #return render(request, 'sdados/esdados.html', context)
    context = {'form': form,'can_edit': can_edit, 'terminas': terminas, "back_to_list": back_to_list} 
    return render(request, 'sdados/esdados.html', context)

@login_required(login_url='userlogin')
@group_required(('DADOS', ))
def csdados(request):
    form = SdadosForm(request.POST)
    print(request.POST)
    print(form.errors)
    if form.is_valid():
        form.save()
        print('Serviço criado com sucesso.')
        return redirect('esdados', pk=form.instance.id)
    context = {'form': form} 
    return render(request, 'sdados/csdados.html', context)

@login_required(login_url='userlogin')
@group_required(('DADOS',))
def csterm(request):
    misid = request.GET.get('misid')
    back_to_list = request.GET.get('back_to_list', '')
    form = StermForm()
    form.fields['misid'].initial = misid
    if request.method == 'POST':
        misid = request.POST.get('misid')
        back_to_list = request.POST.get('back_to_list', '')
        form = StermForm(request.POST)
        if form.is_valid():
            form.save()
            smisid = form.instance.misid
            sd = sdados.objects.filter(isid=smisid).get()

            messages.success(request, 'Terminal adicionado com sucesso.')
            request.method = "GET"
            if back_to_list:
                return redirect(reverse('esdados', kwargs={'pk': sd.id}) + f'?{back_to_list}')
            return redirect('esdados', pk=sd.id)
    context = {'form': form, 'serv': misid, 'back_to_list': back_to_list} 
    return render(request, 'partials/csterm.html', context)

@login_required(login_url='userlogin')
@group_required(('DADOS',))
def esterm(request, pk):
    term = sterm.objects.get(id=pk)
    form = StermForm(instance=term)
    s = form.instance.misid
    sd = sdados.objects.filter(isid=s).get()
    can_edit = request.user.has_perm('sterm.change_sdados' or 'sterm.add_sdados')
    back_to_list = request.GET.get('back_to_list', '')
    if request.method == 'POST' and can_edit:
        form = StermForm(request.POST, instance=term)
        back_to_list = request.POST.get('back_to_list', '')
        if form.is_valid():
            form.save()
            smisid = form.instance.misid
            sd = sdados.objects.filter(isid=smisid).get()
            if back_to_list:
                return redirect(reverse('esdados', kwargs={'pk': sd.id}) + f'?{back_to_list}')
            return redirect('esdados', pk=sd.id)
    context = {'form': form, 'serv': sd.id, 'back_to_list': back_to_list} 
    return render(request, 'partials/esterm.html', context)
