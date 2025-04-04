from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, request
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from extra_views import CreateWithInlinesView
from extra_views import InlineFormSetFactory


from .models import *
from .forms import *


@login_required(login_url='userlogin')
def lista_dados(request):
    l_dados = serv_dados.objects.exclude(Service_status='D')
    context = {'l_dados': l_dados}
    return render(request, 'dados/lista_dados.html', context=context)


@login_required(login_url='userlogin')
def criar_dados(request):
    form = criarservdadosForm(request.POST)
    if form.is_valid():
        d=form.save()
        return redirect('editar_dados', pk=d.id)
    context = {'form':form}
    return render(request, 'dados/criar_dados.html', context=context)

@login_required(login_url='userlogin')
def editar_dados(request, pk):
    lisid = serv_dados.objects.get(id=pk)
    term = lisid.terminacao_set.all()

    form = ServDadosForm(instance=lisid)
    context = {'form': form,
               'term': term
               }
    return render(request, 'dados/editar_dados.html', context=context)

def criar_term(request, pk):
    if request.method == 'POST':
        form = criarterminacaoForm(request.POST or None)
        if form.is_valid():
            terminacao = form.save()
            context = {'terminacao': terminacao}
            return render(request, 'dados/term.html', context )
    return render(request, 'dados/form.html', {'form': criarterminacaoForm()})



