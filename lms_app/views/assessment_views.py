# lms_app/views/assessment_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course
from lms_app.models.assessments import Assignment, AssignmentSubmission, Quiz, QuizAttempt, QuizChoice
from lms_app.forms.assessment_forms import AssignmentSubmissionForm

@login_required
def submit_assignment_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    # Öğrenci bu kursa kayıtlı mı kontrolü eklenebilir...

    # Varsa önceki teslimi bul (Güncelleme yapmak istiyorsa)
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.assignment = assignment
            sub.student = request.user
            sub.save()
            messages.success(request, "Ödeviniz başarıyla teslim edildi!")
            return redirect('course_detail', slug=assignment.course.slug)
    else:
        form = AssignmentSubmissionForm(instance=submission)

    return render(request, 'courses/submit_assignment.html', {'form': form, 'assignment': assignment, 'submission': submission})


@login_required
def take_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        correct_answers = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = QuizChoice.objects.get(id=selected_choice_id)
                if choice.is_correct:
                    correct_answers += 1

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        is_passed = score >= quiz.passing_score

        # Skoru veritabanına kaydet
        QuizAttempt.objects.create(quiz=quiz, student=request.user, score=score, is_passed=is_passed)

        if is_passed:
            messages.success(request, f"Tebrikler! Quizi %{score} başarıyla geçtiniz.")
        else:
            messages.error(request, f"Maalesef quizi geçemediniz. Puanınız: %{score}")

        return redirect('course_detail', slug=quiz.course.slug)

    return render(request, 'courses/take_quiz.html', {'quiz': quiz})