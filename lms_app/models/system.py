from django.db import models
from .users import CustomUser
from .courses import Course  # EKLENDİ


class SystemLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)


# YENİ EKLENEN DUYURU MODELİ
class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title