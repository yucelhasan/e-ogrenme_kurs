from django.shortcuts import get_object_or_404
from django.db.models import Sum
from lms_app.models.interactions import Review, Question
from lms_app.models.ecommerce import OrderItem

def check_user_has_any_review(user):
    """Kullanıcının herhangi bir kursa yorum yapıp yapmadığını kontrol eder."""
    if not user.is_authenticated:
        return False
    return Review.objects.filter(student=user).exists()

def get_course_reviews(course):
    """Kursa ait tüm yorumları öğrenci bilgisiyle birlikte getirir."""
    return Review.objects.filter(course=course).select_related('student').order_by('-id')

def check_user_reviewed_course(user, course):
    """Kullanıcının bu kursa daha önce yorum yapıp yapmadığını kontrol eder."""
    if not user.is_authenticated:
        return False
    return Review.objects.filter(student=user, course=course).exists()

def get_instructor_dashboard_stats(instructor):
    """
    Eğitmenin toplam öğrenci sayısını ve net kazancını hesaplar.
    """
    total_students = OrderItem.objects.filter(
        course__instructor=instructor,
        order__status='completed'
    ).values('order__user').distinct().count()

    gross_income = OrderItem.objects.filter(
        course__instructor=instructor,
        order__status='completed'
    ).aggregate(Sum('price'))['price__sum'] or 0

    net_income = float(gross_income) * 0.80

    return total_students, net_income

def get_lesson_questions(lesson):
    """Bir derse ait tüm soruları ve cevaplarını optimize edilmiş şekilde getirir."""
    return Question.objects.filter(lesson=lesson).prefetch_related('answers', 'answers__user').order_by('-created_at')

def get_question_by_id(question_id):
    """ID bilgisine göre bir soruyu getirir."""
    return get_object_or_404(Question, id=question_id)