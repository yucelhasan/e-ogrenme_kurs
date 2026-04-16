from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Lesson, Enrollment
from lms_app.services.progress_services import mark_lesson_as_completed
from lms_app.services.certificate_services import check_and_generate_certificate

@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    # Kursun ve dersin varlığını kontrol et
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    # Yetki Kontrolü:
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = (course.instructor == request.user)
    is_admin = (request.user.role == 'admin')

    if not (is_enrolled or is_instructor or is_admin):
        messages.error(request, "Bu dersi izlemek için kursa kayıt olmanız gerekmektedir.")
        return redirect('course_detail', slug=course_slug)

    # DERSİ TAMAMLA İŞLEMİ BURADA YAKALANIYOR
    if request.method == 'POST' and is_enrolled:
        # 1. Dersi tamamlandı olarak işaretle
        mark_lesson_as_completed(request.user, lesson)
        
        # 2. İlerlemeyi kontrol et ve gerekiyorsa sertifika üret
        cert_created, certificate = check_and_generate_certificate(request.user, course)

        if cert_created:
            # İlk defa %100 olduysa ve sertifika yeni üretildiyse tebrik mesajı ver
            messages.success(request, f"Tebrikler! Kursu %100 tamamladınız. Sertifika Kodunuz: {certificate.certificate_code}")
        else:
            # Sadece ders tamamlandıysa normal mesaj ver
            messages.success(request, "Ders başarıyla tamamlandı olarak işaretlendi.")

        # İşlem bitince sayfanın yenilenmesi için aynı URL'e yönlendir
        return redirect('lesson_detail', course_slug=course.slug, lesson_id=lesson.id)

    # Yetki tamsa ders sayfasını yükle
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson
    })