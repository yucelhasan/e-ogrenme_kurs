from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Eğitmen'),
        ('student', 'Öğrenci'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon Numarası")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,
                                        verbose_name="Profil Fotoğrafı")
    expertise = models.CharField(max_length=255, blank=True, null=True, verbose_name="Uzmanlık Alanı")

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class InstructorApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'İnceleniyor'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    expertise = models.TextField(verbose_name="Uzmanlık Alanı ve Tecrübe")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"