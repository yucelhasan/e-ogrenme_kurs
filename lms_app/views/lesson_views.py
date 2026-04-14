from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Lesson, Enrollment

@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    # Kursun ve dersin varlığını kontrol et
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    # Yetki Kontrolü:
    # 1. Kullanıcı bu kursa kayıtlı mı?
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    # 2. Kullanıcı bu kursun eğitmeni mi?
    is_instructor = (course.instructor == request.user)
    # 3. Kullanıcı sistem yöneticisi mi?
    is_admin = (request.user.role == 'admin')

    # Eğer yetkisi yoksa, uyar ve detay sayfasına geri gönder
    if not (is_enrolled or is_instructor or is_admin):
        messages.error(request, "Bu dersi izlemek için kursa kayıt olmanız gerekmektedir.")
        return redirect('course_detail', slug=course_slug)

    # Yetki tamsa ders sayfasını yükle
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson
    })