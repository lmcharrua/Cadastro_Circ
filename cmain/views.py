from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

from django.contrib import messages



# Create your views here.
# 
def home(request):

    return redirect("userlogin")

@login_required(login_url='userlogin') 
def main(request):
    return render(request, 'cmain/main.html')

def userlogin(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("main")
    context = {'form':form}
    return render(request, 'cmain/userlogin.html', context=context)


def userlogout(request):

    auth.logout(request)
    # messages.success(request, "Logout success!")
    return redirect("userlogin")

def noperm(request):
    return render(request, 'cmain/noperm.html')