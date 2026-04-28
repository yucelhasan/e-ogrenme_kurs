# lms_app/models/assessments.py
from django.db import models
from .users import CustomUser
from .courses import Course

# --- QUİZ SİSTEMİ MODELLERİ ---
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200, verbose_name="Quiz Başlığı")
    passing_score = models.PositiveIntegerField(default=70, verbose_name="Geçme Notu")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Soru Metni")

    def __str__(self):
        return self.text

class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, verbose_name="Şık Metni")
    is_correct = models.BooleanField(default=False, verbose_name="Doğru Cevap mı?")

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.FloatField(verbose_name="Alınan Puan")
    is_passed = models.BooleanField(verbose_name="Geçti mi?")
    attempted_at = models.DateTimeField(auto_now_add=True)

# --- ÖDEVLENDİRME SİSTEMİ MODELLERİ ---
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200, verbose_name="Ödev Başlığı")
    description = models.TextField(verbose_name="Ödev Açıklaması")
    due_date = models.DateTimeField(verbose_name="Son Teslim Tarihi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/', blank=True, null=True, verbose_name="Yüklenen Dosya")
    text_response = models.TextField(blank=True, null=True, verbose_name="Metin Yanıtı")
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(blank=True, null=True, verbose_name="Not")
    feedback = models.TextField(blank=True, null=True, verbose_name="Eğitmen Geri Bildirimi")

    class Meta:
        unique_together = ('assignment', 'student') # Bir öğrenci bir ödeve tek teslim yapabilir