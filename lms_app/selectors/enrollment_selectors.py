from lms_app.models import Enrollment

def check_enrollment(student, course):
    """Bir öğrencinin belirli bir kursa kayıtlı olup olmadığını kontrol eder."""
    if not student.is_authenticated:
        return False
    return Enrollment.objects.filter(student=student, course=course).exists()

def get_student_enrollments(student):
    """Bir öğrencinin kayıtlı olduğu kursların listesini getirir."""
    if not student.is_authenticated:
        return Enrollment.objects.none()
    return Enrollment.objects.filter(student=student).select_related('course')