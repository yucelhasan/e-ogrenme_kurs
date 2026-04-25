from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Category, Course, Module,
    Lesson, Enrollment, LessonProgress,
    Review, Certificate, SystemLog,
    InstructorApplication
)

# 1. Modülleri kursun içinde satır içi (inline) göstermek için
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

# 2. CustomUser Admin Kaydı (Django'nun kendi UserAdmin'i ile daha güvenli)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('LMS Ek Bilgiler', {'fields': ('role', 'phone', 'profile_picture', 'expertise')}),
    )

# 3. Course Admin Kaydı
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_filter = ('category', 'status')
    search_fields = ('title', 'description')

# 4. YENİ: Eğitmen Başvuruları için Admin Paneli
@admin.register(InstructorApplication)
class InstructorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'user__email', 'expertise')
    readonly_fields = ('user', 'applied_at', 'expertise')

# 5. Diğer Modülleri Kaydet
admin.site.register(Category)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Review)
admin.site.register(Certificate)
admin.site.register(SystemLog)