# lms_app/services/certificate_services.py

import uuid
from lms_app.models import Certificate
from lms_app.selectors.progress_selectors import get_course_progress

def check_and_generate_certificate(user, course):
    """
    Öğrencinin kurs ilerlemesini kontrol eder.
    %100 ise ve henüz sertifika üretilmemişse rastgele benzersiz bir kodla yeni sertifika oluşturur.
    """
    # İlerleme yüzdesini hesapla
    progress = get_course_progress(user, course)

    # İlerleme %100 ise sertifikayı üret
    if progress >= 100:
        # Öğrenciye bu kurs için zaten sertifika verilmiş mi kontrol et
        certificate, created = Certificate.objects.get_or_create(
            student=user,
            course=course,
            defaults={
                # CERT-KursID-KullaniciID-Rastgele8Hane formatında eşsiz bir kod üret
                'certificate_code': f"CERT-{course.id}-{user.id}-{uuid.uuid4().hex[:8].upper()}"
            }
        )
        # created: Eğer yeni oluşturulduysa True, zaten varsa False döner
        return created, certificate

    # %100 değilse
    return False, None