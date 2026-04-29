from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Enrollment
from lms_app.models.ecommerce import Cart, CartItem, Coupon, Order, OrderItem
from django.utils import timezone
from lms_app.services.system_services import create_log # YENİ: Log servisi eklendi


@login_required
def add_to_cart_view(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "Bu kursa zaten kayıtlısınız.")
        return redirect('course_detail', slug=slug)

    if course.price == 0:
        Enrollment.objects.create(student=request.user, course=course)
        # YENİ: Ücretsiz kurs kaydı logu
        create_log(request, "Kursa Kayıt", f"{request.user.username}, '{course.title}' kursuna ücretsiz kayıt oldu.")
        messages.success(request, f"'{course.title}' kursuna ücretsiz kayıt oldunuz! İyi dersler.")
        return redirect('course_detail', slug=slug)

    cart, created = Cart.objects.get_or_create(user=request.user)

    if CartItem.objects.filter(cart=cart, course=course).exists():
        messages.info(request, "Bu kurs zaten sepetinizde bulunuyor.")
    else:
        CartItem.objects.create(cart=cart, course=course)
        messages.success(request, f"'{course.title}' sepetinize eklendi!")

    return redirect('course_detail', slug=slug)


@login_required
def view_cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('course').order_by('-added_at')

    total_price = sum(item.course.price for item in items)
    discount_amount = 0

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code)

            if request.user in coupon.used_by.all():
                messages.warning(request, "Bu kuponu daha önce kullandınız. Her kampanya kodu sadece bir kez kullanılabilir.")
            elif not coupon.is_valid():
                messages.error(request, "Bu kupon kodunun süresi dolmuş veya artık aktif değil.")
            else:
                cart.coupon = coupon
                cart.save()
                messages.success(request, f"Harika! %{coupon.discount_percent} indirim başarıyla uygulandı.")
        except Coupon.DoesNotExist:
            messages.error(request, "Geçersiz bir kupon kodu girdiniz. Lütfen kontrol edip tekrar deneyin.")

    if cart.coupon and total_price > 0:
        discount_amount = (total_price * cart.coupon.discount_percent) / 100

    final_price = total_price - discount_amount

    return render(request, 'ecommerce/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'discount_amount': discount_amount,
        'final_price': final_price
    })


@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.warning(request, "Kurs sepetinizden çıkarıldı.")
    return redirect('view_cart')


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('course').all()

    if not items.exists():
        messages.warning(request, "Sepetiniz boş. Ödeme yapmak için önce kurs eklemelisiniz.")
        return redirect('courses')

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
        # YENİ: Sipariş/Kayıt logu
        create_log(request, "Kursa Kayıt (Sipariş)", f"{request.user.username}, '{item.course.title}' kursunu satın aldı.")

    if cart.coupon:
        cart.coupon.used_by.add(request.user)
        # YENİ: Kupon kullanım logu
        create_log(request, "Kupon Kullanımı", f"{request.user.username}, '{cart.coupon.code}' kuponunu kullandı.")

    items.delete()
    cart.coupon = None
    cart.save()

    messages.success(request, "🎉 Tebrikler! Ödemeniz başarıyla alındı ve kurslara kayıt oldunuz. İyi öğrenmeler!")
    return redirect('profile')