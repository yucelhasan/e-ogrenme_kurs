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

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"