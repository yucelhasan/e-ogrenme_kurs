from django.shortcuts import get_object_or_404
from lms_app.models import Course, CustomUser
from lms_app.models.users import InstructorApplication

def get_instructor_courses(instructor):
    """Eğitmenin verdiği kursları getirir."""
    if not instructor.is_authenticated:
        return Course.objects.none()
    return Course.objects.filter(instructor=instructor).order_by('-created_at')

def get_user_by_username(username):
    """Kullanıcı detaylarını getirir (bulamazsa 404 hatası döndürür)."""
    return get_object_or_404(CustomUser, username=username)

def check_pending_instructor_application(user):
    """Kullanıcının hali hazırda bekleyen bir başvurusu olup olmadığını döner."""
    return InstructorApplication.objects.filter(user=user, status='pending').exists()