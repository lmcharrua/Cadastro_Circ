from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CreateCartasForm, CartaForm
from cmain.decorators import group_required 
import csv, os, tempfile
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from datetime import datetime

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
    campos = [field.name for field in Cartas._meta.fields]
    writer.writerow(campos)

    # Write data rows
    for circ in Cartas.objects.all():
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
    download_name = f"cartas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

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
@group_required(('TX', 'DAT')) 
def lista_cartas(request):
   
    # pesquisa geral
    pesquisar = request.POST.get('search',default='')

    #pesquisa por campos específicos
    filtros = {
    "serial_number__icontains": request.POST.get("serial", ""),
    "part_number__icontains": request.POST.get("part", ""),
    "fabricante__icontains": request.POST.get("fabricante", ""),
    "sistema__icontains": request.POST.get("sistema", ""),
    "b_type__icontains": request.POST.get("board", ""),
    "descricao__icontains": request.POST.get("descr", ""),
    "estado__icontains": request.POST.get("estado", ""),
    "localizacao__icontains": request.POST.get("local", ""),
    "equipamento__icontains": request.POST.get("equip", ""),
    }


    per_page = int(request.POST.get("per_page", 10))
    sort = request.POST.get("sort", "serial_number")  # default sort
    direction = request.POST.get("direction", "asc")

    cartas = Cartas.objects.exclude(estado="ABA")

    resultado = Cartas.objects.filter(
        Q(serial_number__icontains=pesquisar) |
        Q(part_number__icontains=pesquisar) |
        Q(fabricante__icontains=pesquisar) |
        Q(descricao__icontains=pesquisar) |
        Q(sistema__icontains=pesquisar) |
        Q(b_type__icontains=pesquisar) |
        Q(localizacao__icontains=pesquisar) |
        Q(equipamento__icontains=pesquisar)
    ).exclude(estado="ABA")

    for field, value in filtros.items():
        if value:
            resultado = resultado.filter(**{field: value})

    if direction == "desc":
        sort = f"-{sort}"
    resultado = resultado.order_by(sort)

    pages = Paginator(resultado, per_page)
    page_number = request.POST.get('page', 1)

    resultado = pages.get_page(page_number)

    paginas =pages.get_elided_page_range(number=page_number, on_each_side=2, on_ends=2)
    context = {
        'cartas': resultado,
        'per_page': per_page,
        'paginas': paginas,
        "sort": request.POST.get("sort", ""),
        "direction": direction,
        }
    if request.htmx:

        return render(request, 'partials/tabela_c.html', context)
        
    return render(request, 'cartas/lista_cartas.html', context)
