from django.contrib import admin
# Modellerin klasör yapısında olduğu için .models üzerinden hepsini çekiyoruz
from .models import (
    CustomUser, Category, Course, Module,
    Lesson, Enrollment, LessonProgress,
    Review, Certificate, SystemLog
)

# Kullanıcı modelini detaylı görünümlü kaydet
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)

# Diğer modelleri basitçe kaydet
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Review)
admin.site.register(Certificate)
admin.site.register(SystemLog)