# lms_app/views/cart_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Enrollment
from lms_app.models.ecommerce import Cart, CartItem, Coupon, Order, OrderItem
from django.utils import timezone


@login_required
def add_to_cart_view(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')

    # 1. Kullanıcı zaten bu kursa kayıtlı mı?
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "Bu kursa zaten kayıtlısınız.")
        return redirect('course_detail', slug=slug)

    # 2. Kurs ÜCRETSİZ ise sepete atmaya gerek yok, direkt kaydet!
    if course.price == 0:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f"'{course.title}' kursuna ücretsiz kayıt oldunuz! İyi dersler.")
        return redirect('course_detail', slug=slug)

    # 3. Kurs ücretli ise sepete ekle
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Sepette zaten var mı kontrolü
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

    # 1. Ham Toplam Fiyatı Hesapla
    total_price = sum(item.course.price for item in items)
    discount_amount = 0

    # 2. Kupon Kodu Formu Gönderildiyse (POST işlemi)
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code)

            # KONTROL 1: Kullanıcı bu kuponu daha önce kullanmış mı?
            if request.user in coupon.used_by.all():
                messages.warning(request,
                                 "Bu kuponu daha önce kullandınız. Her kampanya kodu sadece bir kez kullanılabilir.")

            # KONTROL 2: Kuponun süresi geçmiş mi veya admin tarafından kapatılmış mı?
            elif not coupon.is_valid():
                messages.error(request, "Bu kupon kodunun süresi dolmuş veya artık aktif değil.")

            # KONTROL 3: Her şey kusursuzsa indirimi uygula!
            else:
                cart.coupon = coupon
                cart.save()
                messages.success(request, f"Harika! %{coupon.discount_percent} indirim başarıyla uygulandı.")

        except Coupon.DoesNotExist:
            # KONTROL 4: Veritabanında böyle bir kod hiç yoksa (Yanlış yazılmışsa)
            messages.error(request, "Geçersiz bir kupon kodu girdiniz. Lütfen kontrol edip tekrar deneyin.")

    # 3. Eğer sepete daha önceden (veya az önce) tanımlanmış bir kupon varsa indirimi hesapla
    if cart.coupon and total_price > 0:
        # İndirim miktarını hesapla: (Toplam * Yüzde) / 100
        discount_amount = (total_price * cart.coupon.discount_percent) / 100

    # 4. Ödenecek Net Tutar
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

    # 1. Sepet boşsa ödeme yapılamaz
    if not items.exists():
        messages.warning(request, "Sepetiniz boş. Ödeme yapmak için önce kurs eklemelisiniz.")
        return redirect('courses')

    # 2. Fiyatları tekrar hesapla (Güvenlik için backend'de son kez hesaplanır)
    total_price = sum(item.course.price for item in items)
    discount_amount = 0

    if cart.coupon and cart.coupon.is_valid() and request.user not in cart.coupon.used_by.all():
        discount_amount = (total_price * cart.coupon.discount_percent) / 100

    final_price = total_price - discount_amount

    # 3. FATURA (Sipariş) OLUŞTURMA
    order = Order.objects.create(
        user=request.user,
        total_amount=total_price,
        discount_amount=discount_amount,
        final_amount=final_price,
        status='completed'
        # Gerçek projede 'pending' yapıp Iyzico/Stripe onayı beklenir. Biz şimdilik direkt tamamlıyoruz.
    )

    # 4. KURSLARI SATIN ALMA VE KAYIT İŞLEMİ
    for item in items:
        # Faturaya kalemi ekle
        OrderItem.objects.create(order=order, course=item.course, price=item.course.price)

        # Öğrenciyi kursa kaydet (Eğer daha önce kayıtlı değilse)
        Enrollment.objects.get_or_create(student=request.user, course=item.course)

    # 5. KUPON KULLANIMINI KAYDET
    if cart.coupon:
        cart.coupon.used_by.add(request.user)

    # 6. SEPETİ TEMİZLE
    items.delete()  # Sepetteki ürünleri sil
    cart.coupon = None  # Sepetteki kuponu kaldır
    cart.save()

    messages.success(request, "🎉 Tebrikler! Ödemeniz başarıyla alındı ve kurslara kayıt oldunuz. İyi öğrenmeler!")
    return redirect('profile')  # Öğrenciyi kurslarını görebilmesi için profiline yönlendiriyoruz