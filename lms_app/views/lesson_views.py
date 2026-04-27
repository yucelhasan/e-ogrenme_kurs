from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Lesson, Enrollment, Question, Answer
from lms_app.forms.interaction_forms import QuestionForm, AnswerForm
from lms_app.services.progress_services import mark_lesson_as_completed
from lms_app.services.certificate_services import check_and_generate_certificate

@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, status='published')
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = (course.instructor == request.user)
    is_admin = (request.user.role == 'admin')

    if not (is_enrolled or is_instructor or is_admin):
        messages.error(request, "Bu dersi izlemek için kayıt olmanız gerekmektedir.")
        return redirect('course_detail', slug=course_slug)

    # SORU SORMA İŞLEMİ
    if request.method == 'POST' and 'ask_question' in request.POST:
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.lesson = lesson
            question.student = request.user
            question.save()
            messages.success(request, "Sorunuz başarıyla iletildi.")
            return redirect('lesson_detail', course_slug=course.slug, lesson_id=lesson.id)

    # DERS TAMAMLA İŞLEMİ
    if request.method == 'POST' and 'complete_lesson' in request.POST and is_enrolled:
        mark_lesson_as_completed(request.user, lesson)
        cert_created, certificate = check_and_generate_certificate(request.user, course)
        if cert_created:
            messages.success(request, f"Tebrikler! Sertifika Kodunuz: {certificate.certificate_code}")
        return redirect('lesson_detail', course_slug=course.slug, lesson_id=lesson.id)

    # Mevcut soruları ve cevapları çek
    questions = Question.objects.filter(lesson=lesson).prefetch_related('answers', 'answers__user').order_by('-created_at')

    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'questions': questions,
        'q_form': QuestionForm(),
        'a_form': AnswerForm(),
    })

# Cevap eklemek için ayrı bir view
@login_required
def add_answer_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            messages.success(request, "Cevabınız eklendi.")
    return redirect('lesson_detail', course_slug=question.lesson.module.course.slug, lesson_id=question.lesson.id)