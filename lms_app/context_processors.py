from lms_app.models.ecommerce import Cart

def cart_processor(request):
    """Giriş yapmış kullanıcının sepetindeki ürün sayısını her sayfaya gönderir."""
    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    return {'cart_count': cart_count}