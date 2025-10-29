from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CircuitoForm, CreateCircuitoForm
from cmain.decorators import group_required 
import csv, os, tempfile
from django.http import HttpResponse, FileResponse
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator


@login_required(login_url='userlogin')
@group_required(('NOC', 'TX', 'DAT', 'DADOS', 'VOZ'))
def ver_circuito(request, pk):
    form = Circuitos.objects.get(id=pk)
    context = {'form':form}
    return render(request, 'circuitos/ver_circuito.html', context=context)

@login_required(login_url='userlogin')
@group_required(('NOC','TX', 'DAT', 'DADOS', 'VOZ'))
def editar_circuito(request, pk):
    cct = Circuitos.objects.get(id=pk)
    form = CircuitoForm(instance=cct)
    criado = form.instance.created_at.strftime('%d-%b-%Y')
    editado = form.instance.updated_at.strftime('%d-%b-%Y')
    can_edit = request.user.has_perm('circuitos.change_circuitos' or 'circuitos.add_circuitos')

    if request.method == 'POST' and can_edit:
        form = CircuitoForm(request.POST,instance=cct)
        if form.is_valid():
            form.instance.update_user = request.user.username
            form.save()
            # messages.success(request, "O circuito foi actualizado com sucesso!")
            print("Circuito actualizado")
            return redirect("lista_cct")  

    context = {'form':form, 'can_edit': can_edit, 'criado': criado, 'editado': editado}
    return render(request, 'circuitos/editar_circuito.html', context=context)

@login_required(login_url='userlogin')
@group_required(('TX', 'DAT', 'DADOS'))
def criar_circuito(request):
    form = CreateCircuitoForm(request.POST)
    if form.is_valid():
        form.instance.create_user = request.user.username
        form.save()
        # messages.success(request, "O circuito foi criado com sucesso!")
        return redirect('editar_circuito', pk=form.instance.id)
    context = {'form':form}
    return render(request, 'circuitos/criar_circuito.html', context=context)

@login_required(login_url='userlogin')
@group_required(('DAT',))
def download(request):
    # Create temporary CSV file
    tmp = tempfile.NamedTemporaryFile(mode="w+", newline="", suffix=".csv", delete=False, encoding="utf-8-sig")
    filepath = tmp.name

    # Configure CSV writer with quotechar='"'
    writer = csv.writer(
        tmp,
        delimiter=';',           # Field separator
        quotechar='"',            # Quote each field with "
        quoting=csv.QUOTE_ALL     # Always quote all fields
    )

    # Write header row
    campos = [field.name for field in Circuitos._meta.fields]
    writer.writerow(campos)

    # Write data rows
    for circ in Circuitos.objects.all():
        row = []
        for field in campos:
            value = getattr(circ, field)
            if value is None:
                value = ""
            elif hasattr(value, "strftime"):
                value = value.strftime("%d-%b-%Y")
            row.append(value)
        writer.writerow(row)

    tmp.close()  # Flush and close temp file

    # Download filename
    download_name = f"circuitos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Stream file to client
    response = FileResponse(open(filepath, "rb"), as_attachment=True, filename=download_name)

    # Delete temporary file after sending
    def cleanup_file(response):
        try:
            os.remove(filepath)
        except OSError:
            pass
        return response

    # Attach cleanup to the response lifecycle
    response._resource_closers.append(lambda: cleanup_file(response))

    return response


@login_required(login_url='userlogin')
@group_required(('NOC', 'TX', 'DAT', 'DADOS', 'VOZ'))
def lista_cct(request):
    pesquisar = request.POST.get('search', '')
    filtros = {
        "N_Circuito__icontains": request.POST.get('N_Circuito', ''),
        "Data_Rate__icontains": request.POST.get('Data_Rate', ''),
        "User_Cct__icontains": request.POST.get('User_Cct', ''),
        "Estado_Cct__icontains": request.POST.get('Estado_Cct', ''),
        "Entidade_PTR1__icontains": request.POST.get('Entidade_PTR1', ''),
        "Morada_PTR1__icontains": request.POST.get('Morada_PTR1', ''),
        "Entidade_PTR2__icontains": request.POST.get('Entidade_PTR2', ''),
        "Morada_PTR2__icontains": request.POST.get('Morada_PTR2', ''),
    }

    per_page = int(request.POST.get('per_page', 10))
    sort = request.POST.get('sort', 'N_Circuito')
    direction = request.POST.get('direction', 'asc')

    l_circuitos = Circuitos.objects.all().exclude(Estado_Cct="Desligado")

    l_circuitos = Circuitos.objects.filter(
        Q(N_Circuito__icontains=pesquisar) |
        Q(Data_Rate__icontains=pesquisar) |
        Q(User_Cct__icontains=pesquisar) |
        Q(Estado_Cct__icontains=pesquisar) |
        Q(Entidade_PTR1__icontains=pesquisar) |
        Q(Morada_PTR1__icontains=pesquisar) |
        Q(Entidade_PTR2__icontains=pesquisar) |
        Q(Morada_PTR2__icontains=pesquisar)
    ).exclude(Estado_Cct="Desligado")
    
    for field, value in filtros.items():
        if value:
            l_circuitos = l_circuitos.filter(**{field: value})

    if direction == 'desc':
        sort = f"-{sort}"
    l_circuitos = l_circuitos.order_by(sort)

    pages = Paginator(l_circuitos, per_page)
    page_number = request.POST.get('page', 1)

    l_circuitos = pages.get_page(page_number)

    paginas = pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=2)
    context = {
        'circuitos': l_circuitos,
        'per_page': per_page,
        'paginas': paginas,
        "sort": request.POST.get("sort", ""),
        "direction": direction,
    }

    if request.htmx:
        return render(request, 'partials/tabela_cct.html', context=context)
    return render(request, 'circuitos/lista_circuitos.html', context)
