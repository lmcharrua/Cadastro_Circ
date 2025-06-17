from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from .models import sdados, sterm
from .forms import sdadosForm, stermForm

@login_required(login_url='userlogin')
def lista_sdados(request):
    lista = sdados.objects.exclude(Service_status='D').order_by('ISID')
    context = {
        'contacts': lista,
    }
    return render(request, 'lista_sdados.html', context)

@login_required(login_url='userlogin')
def detalhe_sdados(request, isid):
    contact = get_object_or_404(sdados, ISID=isid)
    terminations = sterm.objects.filter(misid=contact).order_by('Local')
    
    if request.method == 'POST':
        form = stermForm(request.POST)
        if form.is_valid():
            new_termination = form.save(commit=False)
            new_termination.misid = contact
            new_termination.save()
            return render(request, 'detail_sdados.html', {'contact': contact, 'terminations': terminations, 'form': form})
    else:
        form = stermForm()

    return render(request, 'detail_sdados.html', {'contact': contact, 'terminations': terminations, 'form': form})