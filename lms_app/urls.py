from django.urls import path
from .views import auth_views, course_views, profile_views, instructor_views, lesson_views

urlpatterns = [
    # Ana Sayfa ve Kurs Listesi
    path('', course_views.home_view, name='home'),
    path('kurslar/', course_views.course_list_view, name='courses'),

    # Kurs Detay ve Etkileşim İşlemleri
    path('kurs/<slug:slug>/', course_views.course_detail_view, name='course_detail'),
    path('kurs/<slug:slug>/kayit/', course_views.enroll_course_view, name='enroll_course'),
    path('kurs/<slug:slug>/yorum-yap/', course_views.add_review_view, name='add_review'),

    # Ders İzleme Ekranı
    path('kurs/<slug:course_slug>/ders/<int:lesson_id>/', lesson_views.lesson_detail_view, name='lesson_detail'),

    # Kimlik Doğrulama (Giriş/Çıkış/Kayıt)
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # Öğrenci Profil İşlemleri
    path('profil/', profile_views.profile_view, name='profile'),
    # YENİ EKLENEN: Eğitmenlik Başvurusu URL'i
    path('profil/egitmen-basvurusu/', profile_views.apply_instructor_view, name='apply_instructor'),

    # Eğitmen Paneli
    path('panel/', instructor_views.dashboard_view, name='dashboard'),
    path('panel/kurs-ekle/', instructor_views.add_course_view, name='add_course'),

    path('sistem-yonetimi/', instructor_views.admin_dashboard_view, name='admin_dashboard'),
    path('sistem-yonetimi/basvuru-onayla/<int:app_id>/<str:action>/', instructor_views.approve_application_view, name='approve_application'),
    path('sistem-yonetimi/kurs-onayla/<int:course_id>/<str:action>/', instructor_views.approve_course_view, name='approve_course'),
]