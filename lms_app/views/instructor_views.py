from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, InstructorApplication, Module, Lesson
from lms_app.models.assessments import Quiz, QuizQuestion, QuizChoice, Assignment, AssignmentSubmission
from lms_app.forms.course_forms import CourseForm, ModuleForm, LessonForm
from lms_app.forms.system_forms import AnnouncementForm
from lms_app.forms.assessment_forms import QuizForm, AssignmentForm, GradeSubmissionForm
from lms_app.selectors.user_selectors import get_instructor_courses
from lms_app.selectors.instructor_selectors import get_instructor_dashboard_stats
from lms_app.selectors.system_selectors import get_all_system_logs
from lms_app.services.system_services import create_log
from lms_app.services.instructor_services import (
    handle_instructor_application,
    handle_course_approval,
    delete_course_with_log
)

@login_required
def dashboard_view(request):
    if request.user.role == 'admin': return redirect('admin_dashboard')
    if request.user.role != 'instructor': return redirect('home')

    my_courses = get_instructor_courses(request.user)
    total_students, net_income = get_instructor_dashboard_stats(request.user)

    return render(request, 'admin_panel/dashboard.html', {
        'my_courses': my_courses,
        'total_students': total_students,
        'net_income': net_income
    })

@login_required
def add_course_view(request):
    if request.user.role != 'instructor':
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.status = 'draft'
            course.save()
            create_log(request, "Kurs Eklendi",
                       f"{request.user.username}, '{course.title}' isimli kursu taslak olarak oluşturdu.")

            messages.success(request, "Kursunuz taslak olarak başarıyla oluşturuldu.")
            return redirect('manage_curriculum', course_id=course.id)
        else:
            messages.error(request, "Kurs oluşturulamadı. Lütfen formdaki uyarıları dikkate alarak başlığı değiştirin.")
    else:
        form = CourseForm()

    return render(request, 'admin_panel/add_course.html', {'form': form})

@login_required
def manage_curriculum_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    return render(request, 'admin_panel/manage_curriculum.html', {
        'course': course,
        'module_form': ModuleForm(),
        'lesson_form': LessonForm(),
        'quiz_form': QuizForm(),
        'assignment_form': AssignmentForm()
    })

@login_required
def add_module_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, "Bölüm eklendi!")
    return redirect('manage_curriculum', course_id=course.id)

@login_required
def add_lesson_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, "Ders eklendi!")
    return redirect('manage_curriculum', course_id=module.course.id)

@login_required
def submit_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if not course.modules.exists():
        messages.error(request, "Lütfen önce içerik ekleyin.")
        return redirect('manage_curriculum', course_id=course.id)
    course.status = 'pending'
    course.save()
    messages.success(request, "Kurs onay için gönderildi!")
    return redirect('dashboard')

@login_required
def archive_course_view(request, course_id):
    if request.user.role != 'instructor': return redirect('home')
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    course.status = 'archived'
    course.save()
    messages.info(request, f"{course.title} kursu mağazadan kaldırıldı (Arşivlendi).")
    return redirect('dashboard')

@login_required
def admin_dashboard_view(request):
    if request.user.role != 'admin': return redirect('home')
    pending_applications = InstructorApplication.objects.filter(status='pending')
    pending_courses = Course.objects.filter(status='pending')
    return render(request, 'admin_panel/admin_dashboard.html', {
        'pending_applications': pending_applications,
        'pending_courses': pending_courses
    })

@login_required
def approve_application_view(request, app_id, action):
    if request.user.role != 'admin': return redirect('home')
    app = get_object_or_404(InstructorApplication, id=app_id)
    handle_instructor_application(app, action)
    return redirect('admin_dashboard')

@login_required
def approve_course_view(request, course_id, action):
    if request.user.role != 'admin': return redirect('home')
    course = get_object_or_404(Course, id=course_id)

    if handle_course_approval(request, course, action):
        messages.success(request, "Kurs başarıyla onaylandı ve yayına alındı.")
    else:
        messages.warning(request, "Kurs reddedildi.")
    return redirect('admin_dashboard')

@login_required
def create_announcement_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.course = course
            announcement.instructor = request.user
            announcement.save()
            messages.success(request, "Duyuru başarıyla yayınlandı!")
            return redirect('dashboard')
    else:
        form = AnnouncementForm()
    return render(request, 'admin_panel/create_announcement.html', {'form': form, 'course': course})

@login_required
def add_quiz_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, "Quiz eklendi!")
    return redirect('manage_curriculum', course_id=course.id)

@login_required
def add_assignment_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Ödev sisteme başarıyla eklendi!")
    return redirect('manage_curriculum', course_id=course.id)

@login_required
def manage_quiz_questions_view(request, quiz_id):
    if request.user.role != 'instructor': return redirect('home')
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if question_text:
            question = QuizQuestion.objects.create(quiz=quiz, text=question_text)
            for i in range(1, 5):
                choice_text = request.POST.get(f'choice_{i}')
                is_correct = request.POST.get('correct_choice') == str(i)
                if choice_text:
                    QuizChoice.objects.create(question=question, text=choice_text, is_correct=is_correct)
            messages.success(request, "Soru başarıyla eklendi!")
            return redirect('manage_quiz_questions', quiz_id=quiz.id)
    return render(request, 'admin_panel/manage_quiz.html', {'quiz': quiz})

@login_required
def view_assignment_submissions_view(request, assignment_id):
    if request.user.role != 'instructor': return redirect('home')
    assignment = get_object_or_404(Assignment, id=assignment_id, course__instructor=request.user)
    submissions = assignment.submissions.all().select_related('student').order_by('-submitted_at')
    return render(request, 'admin_panel/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
        'grade_form': GradeSubmissionForm()
    })


@login_required
def grade_submission_view(request, submission_id):
    if request.user.role != 'instructor': return redirect('home')

    submission = get_object_or_404(AssignmentSubmission, id=submission_id, assignment__course__instructor=request.user)

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"{submission.student.username} adlı öğrencinin ödevi notlandırıldı!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Hata ({field}): {error}")

    return redirect('view_assignment_submissions', assignment_id=submission.assignment.id)

@login_required
def admin_system_logs_view(request):
    if request.user.role != 'admin': return redirect('home')
    logs = get_all_system_logs()
    return render(request, 'admin_panel/system_logs.html', {'logs': logs})

@login_required
def edit_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            create_log(request, "Kurs Güncelleme", f"'{course.title}' kurs bilgileri güncellendi.")
            messages.success(request, "Kurs bilgileri başarıyla güncellendi.")
            return redirect('dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_panel/add_course.html', {'form': form, 'edit_mode': True, 'course': course})

@login_required
def delete_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    title = delete_course_with_log(request, course)
    messages.warning(request, f"'{title}' kursu tamamen silindi.")
    return redirect('dashboard')

@login_required
def delete_module_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    course_id = module.course.id
    module_title = module.title
    create_log(request, "Bölüm Silme", f"'{module_title}' bölümü kurstan kaldırıldı.")
    module.delete()
    messages.info(request, "Bölüm başarıyla silindi.")
    return redirect('manage_curriculum', course_id=course_id)

@login_required
def delete_lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    course_id = lesson.module.course.id
    lesson_title = lesson.title
    create_log(request, "Ders Silme", f"'{lesson_title}' dersi müfredattan kaldırıldı.")
    lesson.delete()
    messages.info(request, "Ders başarıyla silindi.")
    return redirect('manage_curriculum', course_id=course_id)