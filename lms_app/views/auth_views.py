from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from axes.decorators import axes_dispatch
from lms_app.forms.auth_forms import CustomUserCreationForm
from lms_app.services.auth_services import (
    register_new_user,
    process_user_login,
    process_failed_login,
    process_user_logout
)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            register_new_user(request, form)
            messages.success(request, "Kaydınız başarıyla tamamlandı!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


@axes_dispatch
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get('remember_me')

            process_user_login(request, user, remember_me)

            messages.info(request, f"Tekrar hoş geldin, {user.username}!")
            return redirect('home')
        else:
            process_failed_login(request)
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    process_user_logout(request)
    messages.warning(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')