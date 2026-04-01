from django.urls import path
from .views import auth_views, course_views, profile_views, instructor_views

urlpatterns = [
    # Kurs İşlemleri
    path('', course_views.home_view, name='home'),
    path('kurslar/', course_views.course_list_view, name='courses'),
    # Kimlik Doğrulama İşlemleri
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # Kullanıcı İşlemleri
    path('profil/', profile_views.profile_view, name='profile'),
    
    # Eğitmen / Admin Paneli İşlemleri
    path('panel/', instructor_views.dashboard_view, name='dashboard'),
    path('panel/kurs-ekle/', instructor_views.add_course_view, name='add_course'),
]