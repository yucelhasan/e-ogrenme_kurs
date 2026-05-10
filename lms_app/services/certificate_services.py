import uuid
from lms_app.models import Certificate
from lms_app.selectors.progress_selectors import get_course_progress

def check_and_generate_certificate(user, course):
    """
    Öğrencinin kurs ilerlemesini kontrol eder.
    %100 ise ve henüz sertifika üretilmemişse rastgele benzersiz bir kodla yeni sertifika oluşturur.
    """
    progress = get_course_progress(user, course)

    if progress >= 100:
        certificate, created = Certificate.objects.get_or_create(
            student=user,
            course=course,
            defaults={
                'certificate_code': f"CERT-{course.id}-{user.id}-{uuid.uuid4().hex[:8].upper()}"
            }
        )
        return created, certificate

    return False, None