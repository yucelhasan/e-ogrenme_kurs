# lms_app/services/progress_services.py

from lms_app.models import LessonProgress


def mark_lesson_as_completed(user, lesson):
    """
    Öğrencinin ilgili dersi tamamladığını veritabanına kaydeder.
    """
    # get_or_create ile kayıt varsa getir, yoksa oluştur
    progress, created = LessonProgress.objects.get_or_create(
        student=user,
        lesson=lesson,
        defaults={'is_completed': True}
    )

    # Eğer kayıt zaten varsa ama False olarak işaretliyse True yap
    if not created and not progress.is_completed:
        progress.is_completed = True
        progress.save()

    return progress