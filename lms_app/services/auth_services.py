from django.contrib.auth import login, logout
from lms_app.services.system_services import create_log

def register_new_user(request, form):
    """Yeni kullanıcıyı kaydeder, giriş yaptırır ve log tutar."""
    user = form.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    create_log(request, "Yeni Kayıt", f"{user.username} sisteme yeni kayıt oldu.")
    return user

def process_user_login(request, user, remember_me):
    """Kullanıcıyı sisteme sokar, session süresini ayarlar ve log tutar."""
    login(request, user)
    create_log(request, "Sisteme Giriş", f"{user.username} başarıyla giriş yaptı.")

    if not remember_me:
        request.session.set_expiry(0)
    else:
        request.session.set_expiry(1209600)  # 2 hafta

def process_failed_login(request):
    """Hatalı giriş denemesini loglar."""
    create_log(request, "Hatalı Giriş Denemesi", "Sisteme hatalı bir giriş denemesi yapıldı. (IP Kaydedildi)")

def process_user_logout(request):
    """Kullanıcı çıkışını yapar ve loglar."""
    create_log(request, "Sistemden Çıkış", f"{request.user.username} oturumu sonlandırdı.")
    logout(request)