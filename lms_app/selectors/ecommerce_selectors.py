from django.shortcuts import get_object_or_404
from django.db.models import Sum
from lms_app.models.ecommerce import Cart, CartItem, Coupon, OrderItem

def get_user_cart(user):
    """Kullanıcıya ait sepeti getirir, yoksa oluşturur."""
    if not user.is_authenticated:
        return None
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def get_cart_items(cart):
    """Sepetteki ürünleri kurs bilgileriyle birlikte getirir."""
    return cart.items.select_related('course').order_by('-added_at')

def check_course_in_cart(cart, course):
    """Belirli bir kursun sepette olup olmadığını kontrol eder."""
    return CartItem.objects.filter(cart=cart, course=course).exists()

def get_cart_item_by_id(item_id, user):
    """ID'ye göre sepetteki ürünü doğrular ve getirir."""
    return get_object_or_404(CartItem, id=item_id, cart__user=user)

def get_coupon_by_code(code):
    """Kupon koduna göre kupon nesnesini getirir."""
    try:
        return Coupon.objects.get(code__iexact=code)
    except Coupon.DoesNotExist:
        return None

def get_instructor_total_students(instructor):
    """Eğitmenin kurslarını satın alan benzersiz öğrenci sayısını döndürür."""
    return OrderItem.objects.filter(
        course__instructor=instructor,
        order__status='completed'
    ).values('order__user').distinct().count()

def get_instructor_gross_income(instructor):
    """Eğitmenin kurslarından elde edilen toplam brüt kazancı hesaplar."""
    return OrderItem.objects.filter(
        course__instructor=instructor,
        order__status='completed'
    ).aggregate(Sum('price'))['price__sum'] or 0