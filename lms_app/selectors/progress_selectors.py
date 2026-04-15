# lms_app/selectors/progress_selectors.py

from django.db.models import Count, Q
from lms_app.models import Lesson, LessonProgress, Course, Enrollment


def get_course_progress(user, course):
    """
    Öğrencinin belirli bir kurstaki % kaç ilerlediğini hesaplayıp getirir.
    """
    # 1. Kurstaki toplam ders sayısını bul
    total_lessons = Lesson.objects.filter(module__course=course).count()

    if total_lessons == 0:
        return 0  # Kursta henüz ders yoksa ilerleme %0'dır

    # 2. Öğrencinin bu kursta 'tamamlandı' (is_completed=True) olarak işaretlediği dersleri bul
    completed_lessons = LessonProgress.objects.filter(
        student=user,
        lesson__module__course=course,
        is_completed=True
    ).count()

    # 3. Yüzdeyi hesapla ve tam sayı olarak döndür
    progress_percentage = (completed_lessons / total_lessons) * 100
    return int(progress_percentage)


def get_user_enrolled_courses_with_progress(user):
    """
    Öğrenci profili için: Öğrencinin kayıtlı olduğu tüm kursları ve ilerleme yüzdelerini liste olarak getirir.
    (student_views.py veya profile_views.py içerisinde kullanılabilir)
    """
    # Öğrencinin kayıtlı olduğu kursları getir (N+1 problemini önlemek için select_related kullanıyoruz)
    enrollments = Enrollment.objects.filter(student=user).select_related('course', 'course__category')

    courses_with_progress = []

    for enrollment in enrollments:
        course = enrollment.course
        progress = get_course_progress(user, course)

        courses_with_progress.append({
            'course': course,
            'enrolled_at': enrollment.enrolled_at,
            'progress': progress
        })

    return courses_with_progress