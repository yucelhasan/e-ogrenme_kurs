from lms_app.models import Enrollment
from lms_app.selectors.enrollment_selectors import check_enrollment

def enroll_user_to_course(user, course):
    if check_enrollment(user, course):
        return False, "Bu kursa zaten kayıtlısınız."

    Enrollment.objects.create(student=user, course=course)
    return True, "Kursa başarıyla kayıt oldunuz! İyi dersler."