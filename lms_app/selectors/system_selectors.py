from lms_app.models import SystemLog, InstructorApplication, Certificate

def get_all_system_logs():
    """Sistemdeki tüm logları en yeniden en eskiye doğru getirir."""
    return SystemLog.objects.all().order_by('-created_at')

def get_pending_instructor_applications():
    """Onay bekleyen eğitmenlik başvurularını getirir."""
    return InstructorApplication.objects.filter(status='pending')

def get_student_certificates(student):
    """Öğrencinin kazandığı sertifikaları getirir."""
    if not student.is_authenticated:
        return []
    return Certificate.objects.filter(student=student).select_related('course')