# lms_app/services/enrollment_services.py
from lms_app.models import Enrollment

def enroll_user_to_course(user, course):
    """
    Kullanıcıyı kursa kaydeder.
    Eğer zaten kayıtlıysa (False, mesaj) döner.
    Başarılıysa (True, mesaj) döner.
    """
    # 1. KURAL: Kullanıcı zaten bu kursa kayıtlı mı?
    if Enrollment.objects.filter(student=user, course=course).exists():
        return False, "Bu kursa zaten kayıtlısınız."

    # 2. KURAL: Kayıtlı değilse yeni kayıt oluştur
    Enrollment.objects.create(student=user, course=course)
    return True, "Kursa başarıyla kayıt oldunuz! İyi dersler."