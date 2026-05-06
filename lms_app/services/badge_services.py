from django.utils import timezone
from datetime import timedelta
from lms_app.selectors.progress_selectors import get_course_progress, get_recent_lesson_progress
from lms_app.selectors.enrollment_selectors import get_student_enrollments
from lms_app.selectors.interaction_selectors import check_user_has_any_review
from lms_app.selectors.course_selectors import get_instructor_published_course_count
from lms_app.selectors.ecommerce_selectors import get_instructor_total_students


def get_user_badges(user):
    badges = []

    if user.role == 'student' or user.role == 'admin':
        if check_user_has_any_review(user):
            badges.append({
                'name': 'Eleştirmen',
                'description': 'İlk kurs değerlendirmesini yaptı.',
                'icon': 'fa-solid fa-comment-dots text-info',
                'bg': 'bg-info-subtle text-info'
            })

        enrollments = get_student_enrollments(user)
        completed_courses = sum(1 for e in enrollments if get_course_progress(user, e.course) == 100)

        if completed_courses >= 5:
            badges.append({
                'name': 'Bilge',
                'description': '5 farklı kursu başarıyla tamamladı.',
                'icon': 'fa-solid fa-book-open-reader text-primary',
                'bg': 'bg-primary-subtle text-primary'
            })

        today = timezone.now().date()
        days_active = set()

        recent_progress = get_recent_lesson_progress(user, days=7)

        for p in recent_progress:
            if p.completed_at:
                days_active.add(p.completed_at.date())

        if (today in days_active and
                (today - timedelta(days=1)) in days_active and
                (today - timedelta(days=2)) in days_active):
            badges.append({
                'name': 'İstikrarlı',
                'description': 'Arka arkaya 3 gün ders çalıştı.',
                'icon': 'fa-solid fa-fire text-danger',
                'bg': 'bg-danger-subtle text-danger'
            })

    if user.role == 'instructor' or user.role == 'admin':
        published_courses = get_instructor_published_course_count(user)

        if published_courses >= 3:
            badges.append({
                'name': 'Üretken',
                'description': '3 veya daha fazla kurs yayınladı.',
                'icon': 'fa-solid fa-layer-group text-success',
                'bg': 'bg-success-subtle text-success'
            })

        total_students = get_instructor_total_students(user)
        if total_students >= 50:
            badges.append({
                'name': 'Popüler',
                'description': f'{total_students} farklı öğrenciye eğitim verdi.',
                'icon': 'fa-solid fa-users text-warning',
                'bg': 'bg-warning-subtle text-warning'
            })

    return badges