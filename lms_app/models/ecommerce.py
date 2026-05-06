from django.db import models
from django.utils import timezone
from .users import CustomUser
from .courses import Course

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Kupon Kodu")
    discount_percent = models.PositiveIntegerField(verbose_name="İndirim Yüzdesi (%)")
    valid_until = models.DateTimeField(verbose_name="Son Geçerlilik Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    used_by = models.ManyToManyField(CustomUser, blank=True, related_name='used_coupons', verbose_name="Kullananlar")

    def is_valid(self):
        """Kuponun süresinin geçip geçmediğini ve aktifliğini kontrol eder"""
        return self.is_active and self.valid_until >= timezone.now()

    def __str__(self):
        return f"{self.code} - %{self.discount_percent} İndirim"

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Sepeti"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'course')

    def __str__(self):
        return f"{self.cart.user.username} - {self.course.title}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ödeme Bekleniyor'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Başarısız'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Tutar")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="İndirim Tutarı")
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ödenen Net Tutar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satın Alınan Fiyat")

    def __str__(self):
        return f"#{self.order.id} - {self.course.title}"