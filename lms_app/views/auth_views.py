from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from lms_app.forms.auth_forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kaydınız başarıyla tamamlandı!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


# lms_app/views/auth_views.py

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # "Beni Hatırla" kontrolü
            remember_me = request.POST.get('remember_me')
            if not remember_me:
                # İşaretlenmediyse: settings.py'deki gibi tarayıcı kapandığında oturum düşer
                request.session.set_expiry(0)
            else:
                # İşaretlendiyse: Oturum 14 gün (1.209.600 saniye) açık kalır
                request.session.set_expiry(1209600)

            messages.info(request, f"Tekrar hoş geldin, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.warning(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')