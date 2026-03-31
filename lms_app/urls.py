from django.urls import path
from .views import auth_views, course_views, profile_views

urlpatterns = [
    # Kurs İşlemleri
    path('', course_views.home_view, name='home'),

    # Kimlik Doğrulama İşlemleri
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # Kullanıcı İşlemleri
    path('profil/', profile_views.profile_view, name='profile'),
]