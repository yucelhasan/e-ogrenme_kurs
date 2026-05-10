from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.selectors.course_selectors import get_published_course_by_slug
from lms_app.selectors.ecommerce_selectors import get_user_cart, get_cart_items, get_coupon_by_code
from lms_app.services.ecommerce_services import (
    process_add_to_cart,
    apply_coupon_to_cart,
    remove_item_from_cart,
    process_checkout
)


@login_required
def add_to_cart_view(request, slug):
    course = get_published_course_by_slug(slug)

    success, message, msg_type = process_add_to_cart(request, course)

    if msg_type == "warning":
        messages.warning(request, message)
    elif msg_type == "info":
        messages.info(request, message)
    else:
        messages.success(request, message)

    return redirect('course_detail', slug=slug)


@login_required
def view_cart_view(request):
    cart = get_user_cart(request.user)
    items = get_cart_items(cart)

    total_price = sum(item.course.price for item in items)
    discount_amount = 0

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        coupon = get_coupon_by_code(coupon_code)

        success, message = apply_coupon_to_cart(request, cart, coupon)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

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
    remove_item_from_cart(request, item_id)
    messages.warning(request, "Kurs sepetinizden çıkarıldı.")
    return redirect('view_cart')

@login_required
def checkout_view(request):
    cart = get_user_cart(request.user)
    items = get_cart_items(cart)

    if not items.exists():
        messages.warning(request, "Sepetiniz boş. Ödeme yapmak için önce kurs eklemelisiniz.")
        return redirect('courses')

    total_price = sum(item.course.price for item in items)
    discount_amount = 0
    if cart.coupon and total_price > 0:
        discount_amount = (total_price * cart.coupon.discount_percent) / 100
    final_price = total_price - discount_amount

    if request.method == 'POST':

        process_checkout(request, cart, items)
        messages.success(request, "🎉 Tebrikler! Ödemeniz başarıyla alındı ve kurslara kayıt oldunuz. İyi öğrenmeler!")
        return redirect('profile')

    return render(request, 'ecommerce/checkout.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'discount_amount': discount_amount,
        'final_price': final_price
    })