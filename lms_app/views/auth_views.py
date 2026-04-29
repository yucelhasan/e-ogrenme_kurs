from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from axes.decorators import axes_dispatch
from lms_app.forms.auth_forms import CustomUserCreationForm
from lms_app.services.system_services import create_log # Zaten vardı

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            create_log(request, "Yeni Kayıt", f"{user.username} sisteme yeni kayıt oldu.")
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
            login(request, user)
            create_log(request, "Sisteme Giriş", f"{user.username} başarıyla giriş yaptı.")

            remember_me = request.POST.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)

            messages.info(request, f"Tekrar hoş geldin, {user.username}!")
            return redirect('home')
        else:
            # YENİ: Hatalı Giriş Logu
            create_log(request, "Hatalı Giriş Denemesi", f"Sisteme hatalı bir giriş denemesi yapıldı. (IP Kaydedildi)")
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    create_log(request, "Sistemden Çıkış", f"{request.user.username} oturumu sonlandırdı.")
    logout(request)
    messages.warning(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')