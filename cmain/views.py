from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .forms import LoginForm, ChangePasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import PasswordHistory


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

@login_required
def custom_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # 1️⃣ Validate current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'cmain/change_password.html')

        # 2️⃣ Match new passwords
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'cmain/change_password.html')

        # 3️⃣ Validate strength (Django’s validators already handle uppercase, digits, etc.)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'cmain/change_password.html')

        # 4️⃣ Prevent reuse of last 5 passwords
        last_passwords = PasswordHistory.objects.filter(user=user).order_by('-created_at')[:5]
        for old in last_passwords:
            if check_password(new_password, old.password):
                messages.error(request, "You cannot reuse any of your last 5 passwords.")
                return render(request, 'cmain/change_password.html')

        # 5️⃣ Change password and save
        user.set_password(new_password)
        user.save()

        # 6️⃣ Store the new password in history
        PasswordHistory.objects.create(user=user, password=user.password)

        # 7️⃣ Trim to last 5 records
        old_entries = PasswordHistory.objects.filter(user=user).order_by('-created_at')[5:]
        if old_entries.exists():
            old_entries.delete()

        # 8️⃣ Keep the user logged in
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been successfully changed.")
        return redirect('main')

    return render(request, 'cmain/change_password.html')

# def custom_change_password(request):
#     if request.method == 'POST':
#         current_password = request.POST.get('current_password')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         user = request.user

#         # 1️⃣ Validate current password
#         if not user.check_password(current_password):
#             messages.error(request, "Current password is incorrect.")
#             return render(request, 'cmain/change_password.html')

#         # 2️⃣ Check new passwords match
#         if new_password != confirm_password:
#             messages.error(request, "New passwords do not match.")
#             return render(request, 'cmain/change_password.html')

#         # 3️⃣ Validate password strength (optional)
#         if len(new_password) < 8:
#             messages.error(request, "New password must be at least 8 characters.")
#             return render(request, 'cmain/change_password.html')

#         # 4️⃣ Set new password
#         try:
#             validate_password(new_password, user)
#         except ValidationError as e:
#             for error in e.messages:
#                 messages.error(request, error)
#             return render(request, 'cmain/change_password.html')
#         user.set_password(new_password)
#         user.save()

#         # 5️⃣ Keep the user logged in after password change
#         update_session_auth_hash(request, user)

#         #messages.success(request, "Your password has been successfully changed.")
#         return redirect('main')  # redirect wherever you want

#     return render(request, 'cmain/change_password.html')