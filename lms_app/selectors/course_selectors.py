from lms_app.models import Course

def get_active_courses():
    """
    Ana sayfa için aktif kursları getirir.
    select_related ile N+1 sorgu problemini çözer.
    """
    return Course.objects.filter(is_active=True).select_related('category', 'instructor').order_by('-created_at')