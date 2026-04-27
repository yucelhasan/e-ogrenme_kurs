from django.db import models
from .users import CustomUser
from .courses import Course, Lesson # Lesson EKLENDİ

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

class Certificate(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_code = models.CharField(max_length=100, unique=True)

# YENİ EKLENEN SORU-CEVAP MODELLERİ
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # Öğrenci veya Eğitmen
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)