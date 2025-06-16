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
               'term': term,
               'tt'  : pk,
               }
    return render(request, 'dados/editar_dados.html', context=context)

@login_required(login_url='userlogin')
def criar_term(request):
    if request.method == 'POST':
        form1 = ServDadosForm(request.POST or None)
        form = criarterminacaoForm(request.POST or None)

        if form.is_valid():
            term = form.save()
            context = {'t': term}
            
            return render(request, 'dados/linha_term.html', context ) 
        else:
            print(form1.errors)
            print(form.errors)
    else:
        net = request.GET.get('id')
        cform = criarterminacaoForm(None)
        context = {'form': cform, 
                   'next': net}
        
        return render(request, 'dados/form.html', context=context)
# a chamada ao view tem que incluir o ISID que deve ser passado no context para o template


