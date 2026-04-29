# lms_app/services/system_services.py
from lms_app.models import SystemLog

def create_log(request, action, details=None):
    """Sistemdeki önemli olayları veritabanına kaydeder."""
    # Kullanıcının IP adresini al
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    SystemLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        details=details,
        ip_address=ip
    )