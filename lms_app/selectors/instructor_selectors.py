from django.db.models import Sum
from lms_app.models.ecommerce import OrderItem


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