from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.interaction_forms import QuestionForm, AnswerForm
from lms_app.selectors.course_selectors import get_published_course_by_slug, get_lesson_by_id_and_course
from lms_app.selectors.enrollment_selectors import check_enrollment
from lms_app.selectors.interaction_selectors import get_lesson_questions, get_question_by_id
from lms_app.services.progress_services import mark_lesson_as_completed
from lms_app.services.certificate_services import check_and_generate_certificate
from lms_app.services.system_services import create_log
from lms_app.services.interaction_services import create_question, create_answer
from django.shortcuts import get_object_or_404
from lms_app.models.interactions import Answer


@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    course = get_published_course_by_slug(course_slug)
    lesson = get_lesson_by_id_and_course(lesson_id, course)
    is_enrolled = check_enrollment(request.user, course)

    is_instructor = (course.instructor == request.user)
    is_admin = (request.user.role == 'admin')

    if not (is_enrolled or is_instructor or is_admin):
        messages.error(request, "Bu dersi izlemek için kayıt olmanız gerekmektedir.")
        return redirect('course_detail', slug=course_slug)

    if request.method == 'POST' and 'ask_question' in request.POST:
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            create_question(request.user, lesson, q_form)
            messages.success(request, "Sorunuz başarıyla iletildi.")
            return redirect('lesson_detail', course_slug=course.slug, lesson_id=lesson.id)

    if request.method == 'POST' and 'complete_lesson' in request.POST and is_enrolled:
        mark_lesson_as_completed(request.user, lesson)
        cert_created, certificate = check_and_generate_certificate(request.user, course)
        if cert_created:
            create_log(request, "Sertifika Kazanımı",
                       f"{request.user.username}, '{course.title}' kursunu tamamlayarak sertifika kazandı.")
            messages.success(request, f"Tebrikler! Sertifika Kodunuz: {certificate.certificate_code}")
        return redirect('lesson_detail', course_slug=course.slug, lesson_id=lesson.id)

    questions = get_lesson_questions(lesson)

    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'questions': questions,
        'q_form': QuestionForm(),
        'a_form': AnswerForm(),
    })


@login_required
def add_answer_view(request, question_id):
    question = get_question_by_id(question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            create_answer(request.user, question, form)
            messages.success(request, "Cevabınız eklendi.")

    return redirect('lesson_detail', course_slug=question.lesson.module.course.slug, lesson_id=question.lesson.id)

@login_required
def delete_answer_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    course = answer.question.lesson.module.course
    
    # Yetki kontrolü: Yorumun sahibi, kurs eğitmeni veya admin silebilir
    is_author = (request.user == answer.user)
    is_instructor = (request.user == course.instructor)
    is_admin = (request.user.role == 'admin')
    
    if is_author or is_instructor or is_admin:
        answer.delete()
        messages.success(request, "Yorum başarıyla silindi.")
    else:
        messages.error(request, "Bu yorumu silme yetkiniz bulunmuyor.")
        
    return redirect('lesson_detail', course_slug=course.slug, lesson_id=answer.question.lesson.id)