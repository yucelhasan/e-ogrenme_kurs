from lms_app.services.system_services import create_log

def update_user_profile(request, form):
    """Kullanıcı profilini günceller ve log kaydı oluşturur."""
    user = form.save()
    create_log(request, "Profil Güncelleme", f"{user.username} profil bilgilerini güncelledi.")
    return user

def submit_instructor_application(request, form):
    """Eğitmenlik başvurusunu kullanıcıyla ilişkilendirerek kaydeder."""
    application = form.save(commit=False)
    application.user = request.user
    application.save()
    return application