from django.db import models
from .users import CustomUser
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # allow_unicode=True ile Türkçe karakterleri daha iyi anlar
            base_slug = slugify(self.name, allow_unicode=True)

            # Eğer isimden slug üretemezse (sadece sembol girildiyse vs.)
            # Rastgele 8 haneli benzersiz bir slug üretir, DB'nin çökmesini %100 engeller.
            if not base_slug:
                base_slug = f"kategori-{uuid.uuid4().hex[:8]}"

            self.slug = base_slug
        super().save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs Başlığı")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Açıklama")

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='taught_courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Yeni eklediğimiz Kapak Fotoğrafı alanı
    image = models.ImageField(upload_to='course_images/', null=True, blank=True, verbose_name="Kapak Resmi")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    class Meta: ordering = ['order']

    def __str__(self): return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, help_text="Örn: 10:45")

    def __str__(self): return self.title