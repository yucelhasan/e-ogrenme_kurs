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
    is_private = models.BooleanField(default=False, verbose_name="Gizli Profil")  # YENİ EKLENEN

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

class Connection(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friendship_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"