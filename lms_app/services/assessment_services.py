from lms_app.models.assessments import QuizAttempt
from lms_app.selectors.assessment_selectors import get_quiz_choice_by_id

def evaluate_quiz_and_save_attempt(quiz, student, post_data):
    """
    Öğrencinin quiz cevaplarını hesaplar, geçip geçmediğini bulur
    ve sonucu veritabanına yazar.
    """
    correct_answers = 0
    total_questions = quiz.questions.count()

    for question in quiz.questions.all():
        selected_choice_id = post_data.get(f'question_{question.id}')
        if selected_choice_id:
            choice = get_quiz_choice_by_id(selected_choice_id)
            if choice and choice.is_correct:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    is_passed = score >= quiz.passing_score

    QuizAttempt.objects.create(quiz=quiz, student=student, score=score, is_passed=is_passed)

    return score, is_passed