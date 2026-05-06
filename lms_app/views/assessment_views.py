from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.assessment_forms import AssignmentSubmissionForm
from lms_app.selectors.assessment_selectors import get_assignment_by_id, get_student_submission, get_quiz_by_id
from lms_app.services.assessment_services import evaluate_quiz_and_save_attempt

@login_required
def submit_assignment_view(request, assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    submission = get_student_submission(assignment, request.user)

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
    quiz = get_quiz_by_id(quiz_id)

    if request.method == 'POST':
        score, is_passed = evaluate_quiz_and_save_attempt(quiz, request.user, request.POST)

        if is_passed:
            messages.success(request, f"Tebrikler! Quizi %{score} başarıyla geçtiniz.")
        else:
            messages.error(request, f"Maalesef quizi geçemediniz. Puanınız: %{score}")

        return redirect('course_detail', slug=quiz.course.slug)

    return render(request, 'courses/take_quiz.html', {'quiz': quiz})