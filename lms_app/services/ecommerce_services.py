from lms_app.models import Enrollment
from lms_app.models.ecommerce import CartItem, Order, OrderItem
from lms_app.services.system_services import create_log
from lms_app.selectors.enrollment_selectors import check_enrollment
from lms_app.selectors.ecommerce_selectors import get_user_cart, check_course_in_cart, get_cart_item_by_id


def process_add_to_cart(request, course):
    """Kursa kayıt olma veya sepete ekleme işlemlerini yönetir."""

    if check_enrollment(request.user, course):
        return False, "Bu kursa zaten kayıtlısınız.", "warning"

    if course.price == 0:
        Enrollment.objects.create(student=request.user, course=course)
        create_log(request, "Kursa Kayıt", f"{request.user.username}, '{course.title}' kursuna ücretsiz kayıt oldu.")
        return True, f"'{course.title}' kursuna ücretsiz kayıt oldunuz! İyi dersler.", "success"

    cart = get_user_cart(request.user)

    if check_course_in_cart(cart, course):
        return False, "Bu kurs zaten sepetinizde bulunuyor.", "info"

    CartItem.objects.create(cart=cart, course=course)
    return True, f"'{course.title}' sepetinize eklendi!", "success"


def apply_coupon_to_cart(request, cart, coupon):
    """Sepete kupon uygulama mantığını yönetir."""
    if not coupon:
        return False, "Geçersiz bir kupon kodu girdiniz. Lütfen kontrol edip tekrar deneyin."

    if request.user in coupon.used_by.all():
        return False, "Bu kuponu daha önce kullandınız. Her kampanya kodu sadece bir kez kullanılabilir."

    if not coupon.is_valid():
        return False, "Bu kupon kodunun süresi dolmuş veya artık aktif değil."

    cart.coupon = coupon
    cart.save()
    return True, f"Harika! %{coupon.discount_percent} indirim başarıyla uygulandı."


def remove_item_from_cart(request, item_id):
    """Sepetten ürün silme işlemini yönetir."""
    item = get_cart_item_by_id(item_id, request.user)
    item.delete()


def process_checkout(request, cart, items):
    """Ödeme işlemini tamamlar, siparişi oluşturur ve kullanıcıyı kurslara kaydeder."""
    total_price = sum(item.course.price for item in items)
    discount_amount = 0

    if cart.coupon and cart.coupon.is_valid() and request.user not in cart.coupon.used_by.all():
        discount_amount = (total_price * cart.coupon.discount_percent) / 100

    final_price = total_price - discount_amount

    order = Order.objects.create(
        user=request.user,
        total_amount=total_price,
        discount_amount=discount_amount,
        final_amount=final_price,
        status='completed'
    )

    for item in items:
        OrderItem.objects.create(order=order, course=item.course, price=item.course.price)
        Enrollment.objects.get_or_create(student=request.user, course=item.course)
        create_log(request, "Kursa Kayıt (Sipariş)",
                   f"{request.user.username}, '{item.course.title}' kursunu satın aldı.")

    if cart.coupon:
        cart.coupon.used_by.add(request.user)
        create_log(request, "Kupon Kullanımı", f"{request.user.username}, '{cart.coupon.code}' kuponunu kullandı.")

    items.delete()
    cart.coupon = None
    cart.save()