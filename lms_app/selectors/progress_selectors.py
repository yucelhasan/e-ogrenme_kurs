# lms_app/selectors/progress_selectors.py

from django.db.models import Count, Q
from lms_app.models import Lesson, LessonProgress, Course, Enrollment


def get_course_progress(user, course):
    """
    Öğrencinin belirli bir kurstaki % kaç ilerlediğini hesaplayıp getirir.
    """
    total_lessons = Lesson.objects.filter(module__course=course).count()

    if total_lessons == 0:
        return 0

    completed_lessons = LessonProgress.objects.filter(
        student=user,
        lesson__module__course=course,
        is_completed=True
    ).count()

    progress_percentage = (completed_lessons / total_lessons) * 100
    return int(progress_percentage)


def get_user_enrolled_courses_with_progress(user):
    """
    Öğrenci profili için: Öğrencinin kayıtlı olduğu tüm kursları ve ilerleme yüzdelerini liste olarak getirir.
    (student_views.py veya profile_views.py içerisinde kullanılabilir)
    """
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


def get_recent_lesson_progress(user, days):
    from django.utils import timezone
    from datetime import timedelta
    from lms_app.models import LessonProgress

    if not user.is_authenticated:
        return []

    today = timezone.now().date()
    return LessonProgress.objects.filter(
        student=user,
        is_completed=True,
        completed_at__gte=today - timedelta(days=days)
    )