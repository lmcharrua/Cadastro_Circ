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
# def lista_cartas(request):
#     cartas = Cartas.objects.exclude(estado="ABA").order_by('fabricante', 'part_number', 'serial_number')
#     return render(request, 'cartas/lista_cartas.html', {'cartas': cartas})  
def lista_cartas(request):
    """
    Server-side view for the Carta list with HTMX.
    Supports pagination, sorting, global and per-column search.
    """

    # --- Query parameters ---
    search_global = request.GET.get("search", "")
    filters = {
        "serial_number__icontains": request.GET.get("serial_number", ""),
        "part_number__icontains": request.GET.get("part_number", ""),
        "fabricante__icontains": request.GET.get("fabricante", ""),
        "sistema__icontains": request.GET.get("sistema", ""),
        "b_type__icontains": request.GET.get("b_type", ""),
        "descricao__icontains": request.GET.get("descricao", ""),
        "estado__icontains": request.GET.get("estado", ""),
        "localizacao__icontains": request.GET.get("localizacao", ""),
        "equipamento__icontains": request.GET.get("equipamento", ""),
    }

    sort = request.GET.get("sort", "serial_number")
    direction = request.GET.get("direction", "asc")
    per_page = int(request.GET.get("per_page", 25))

    # --- Base queryset ---
    cartas = Cartas.objects.exclude(estado="ABA")

    # --- Global search ---
    if search_global:
        cartas = cartas.filter(
            Q(serial_number__icontains=search_global)
            | Q(part_number__icontains=search_global)
            | Q(fabricante__icontains=search_global)
            | Q(descricao__icontains=search_global)
            | Q(sistema__icontains=search_global)
            | Q(b_type__icontains=search_global)
            | Q(localizacao__icontains=search_global)
            | Q(equipamento__icontains=search_global)
        )

    # --- Per-column filters ---
    for field, value in filters.items():
        if value:
            cartas = cartas.filter(**{field: value})

    # --- Sorting ---
    if direction == "desc":
        sort = f"-{sort}"
    cartas = cartas.order_by(sort)

    # --- Pagination ---
    paginator = Paginator(cartas, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # --- Context ---
    context = {
        "page_obj": page_obj,
        "sort": request.GET.get("sort", ""),
        "direction": direction,
        "per_page": per_page,
        "page_sizes": [10, 25, 50, 100],
        "columns": [
            ("N. Série", "serial_number"),
            ("Part Number", "part_number"),
            ("Fabricante", "fabricante"),
            ("Sistema", "sistema"),
            ("Board Type", "b_type"),
            ("Descrição", "descricao"),
            ("Estado", "estado"),
            ("Localização", "localizacao"),
            ("Equipamento", "equipamento"),
        ],
    }

    # --- Return partial or full page ---
    if request.htmx:
        return render(request, "partials/_tabela_cartas.html", context)
    return render(request, "cartas/lista_cartas.html", context)



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


    # response = HttpResponse(
    #     content_type='text/csv',
    #     headers={'Content-Disposition': 'attachment; filename="cartas.csv"'},
    # )

    # writer = csv.writer(response)
    # writer.writerow(['Fabricante', 'Data Receção', 'Tipo', 'Part Number', 'Serial Number', 'Descrição', 'Estado', 'Projeto', 'Sistema', 'Localização', 'Equipamento', 'Subrack', 'Slot', 'Porto', 'Observações'])

    # cartas = Cartas.objects.all().values_list('fabricante', 'data_rececao', 'b_type', 'part_number', 'serial_number', 'descricao', 'estado', 'projeto', 'sistema', 'localizacao', 'equipamento', 'subrack', 'slot', 'porto', 'observacoes')
    # for carta in cartas:
    #     writer.writerow(carta)

    # return response