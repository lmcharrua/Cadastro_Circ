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
#from csv_export.views import CSVExportView


@login_required(login_url='userlogin')
@group_required(('NOC', 'TX', 'DAT', 'DADOS', 'VOZ'))
def lista_cct(request):
    l_circuitos= Circuitos.objects.exclude(Estado_Cct="Desligado")
    context = {'circuitos': l_circuitos}

    return render(request, 'circuitos/lista_circuitos.html', context=context)

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

# def download(request):
#     data = Circuitos.objects.all()

#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": 'attachment; filename="circuitos.csv"'},
#     )

#     writer = csv.writer(response, delimiter=';')
#     campos = [f.name for f in Circuitos._meta.fields]
#     writer.writerow(campos)  # CSV header

#     # 
#     for circ in data:

#          writer.writerow([circ.id, circ.N_Circuito, circ.Data_Rate, circ.Data_Inst, circ.Data_Activ, circ.Estado_Cct,
#                circ.Entidade_PTR1, circ.Morada_PTR1, circ.Cod_Post_PTR1, circ.Interface_PTR1,
#                circ.Equip_PTR1, circ.Slot_PTR1, circ.Trib_PTR1,
#                circ.Entidade_PTR2, circ.Morada_PTR2, circ.Cod_Post_PTR2, circ.Interface_PTR2,
#                circ.Equip_PTR2, circ.Slot_PTR2, circ.Trib_PTR2,
#                circ.User_Cct, circ.Propriedade_Cct, circ.Outras_Ref,
#                circ.created_at.strftime('%d-%b-%Y'), circ.updated_at.strftime('%d-%b-%Y'),
#                circ.update_user, circ.create_user])

#     return response



# class downteste(CSVExportView):
#     model = Circuitos
#     fields = "__all__"