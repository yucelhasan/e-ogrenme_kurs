# lms_app/services/badge_services.py
from django.utils import timezone
from datetime import timedelta
from lms_app.models import Review, Course, Enrollment, LessonProgress
from lms_app.selectors.progress_selectors import get_course_progress

def get_user_badges(user):
    """Kullanıcının rolüne göre hak ettiği rozetleri hesaplar ve döndürür."""
    badges = []

    # --- ÖĞRENCİ ROZETLERİ ---
    if user.role == 'student' or user.role == 'admin':
        # 1. ELEŞTİRMEN ROZETİ: En az 1 yorum yapmışsa
        if Review.objects.filter(student=user).exists():
            badges.append({
                'name': 'Eleştirmen',
                'description': 'İlk kurs değerlendirmesini yaptı.',
                'icon': 'fa-solid fa-comment-dots text-info',
                'bg': 'bg-info-subtle text-info'
            })
            
        # 2. BİLGE ROZETİ: En az 5 kursu %100 tamamlamışsa
        enrollments = Enrollment.objects.filter(student=user)
        completed_courses = sum(1 for e in enrollments if get_course_progress(user, e.course) == 100)
        
        if completed_courses >= 5:
            badges.append({
                'name': 'Bilge',
                'description': '5 farklı kursu başarıyla tamamladı.',
                'icon': 'fa-solid fa-book-open-reader text-primary',
                'bg': 'bg-primary-subtle text-primary'
            })

        # 3. İSTİKRARLI ROZETİ: Son 3 gün üst üste ders tamamlamışsa
        today = timezone.now().date()
        days_active = set()
        
        # Öğrencinin son 7 gündeki ders ilerlemelerini al
        recent_progress = LessonProgress.objects.filter(
            student=user, 
            is_completed=True,
            completed_at__gte=today - timedelta(days=7)
        )
        
        for p in recent_progress:
            if p.completed_at:
                days_active.add(p.completed_at.date())
                
        # 3 gün arka arkaya girip girmediğini kontrol et
        if (today in days_active and 
            (today - timedelta(days=1)) in days_active and 
            (today - timedelta(days=2)) in days_active):
            badges.append({
                'name': 'İstikrarlı',
                'description': 'Arka arkaya 3 gün ders çalıştı.',
                'icon': 'fa-solid fa-fire text-danger',
                'bg': 'bg-danger-subtle text-danger'
            })

    # --- EĞİTMEN ROZETLERİ ---
    if user.role == 'instructor' or user.role == 'admin':
        published_courses = Course.objects.filter(instructor=user, status='published').count()
        
        # 1. ÜRETKEN EĞİTMEN ROZETİ: 3 ve üzeri kurs yayınlamışsa
        if published_courses >= 3:
            badges.append({
                'name': 'Üretken',
                'description': '3 veya daha fazla kurs yayınladı.',
                'icon': 'fa-solid fa-layer-group text-success',
                'bg': 'bg-success-subtle text-success'
            })
            
        # 2. POPÜLER EĞİTMEN ROZETİ: Toplam 50'den fazla farklı öğrencisi varsa
        total_students = Enrollment.objects.filter(course__instructor=user).values('student').distinct().count()
        if total_students >= 50:
            badges.append({
                'name': 'Popüler',
                'description': f'{total_students} farklı öğrenciye eğitim verdi.',
                'icon': 'fa-solid fa-users text-warning',
                'bg': 'bg-warning-subtle text-warning'
            })

    return badges