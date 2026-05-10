from django.shortcuts import get_object_or_404
from lms_app.models.assessments import Assignment, AssignmentSubmission, Quiz, QuizChoice

def get_assignment_by_id(assignment_id):
    """Verilen ID'ye göre ödevi getirir."""
    return get_object_or_404(Assignment, id=assignment_id)

def get_student_submission(assignment, student):
    """Öğrencinin bu ödeve daha önce yaptığı teslimi getirir."""
    if not student.is_authenticated:
        return None
    return AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()

def get_quiz_by_id(quiz_id):
    """Verilen ID'ye göre quizi getirir."""
    return get_object_or_404(Quiz, id=quiz_id)

def get_quiz_choice_by_id(choice_id):
    """Seçilen şıkkı veritabanından bulur."""
    try:
        return QuizChoice.objects.get(id=choice_id)
    except QuizChoice.DoesNotExist:
        return None