from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Category, Course, Module,
    Lesson, Enrollment, LessonProgress,
    Review, Certificate, SystemLog,
    InstructorApplication,Coupon, Cart, Order, OrderItem
)

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('LMS Ek Bilgiler', {'fields': ('role', 'phone', 'profile_picture', 'expertise')}),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_filter = ('category', 'status')
    search_fields = ('title', 'description')

@admin.register(InstructorApplication)
class InstructorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'user__email', 'expertise')
    readonly_fields = ('user', 'applied_at', 'expertise')
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_until', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('course', 'price') # Fatura değiştirilemez

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'final_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total_amount', 'discount_amount', 'final_amount', 'status')

admin.site.register(Category)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Review)
admin.site.register(Certificate)
admin.site.register(SystemLog)