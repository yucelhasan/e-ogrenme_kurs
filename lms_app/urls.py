from django.urls import path
from .views import auth_views, course_views, profile_views, instructor_views, lesson_views

# YENİ IMPORT: Django'nun hazır auth view'larını "django_auth_views" adıyla içeri alıyoruz
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    # --- KURS VE ANA SAYFA İŞLEMLERİ ---
    path('', course_views.home_view, name='home'),
    path('kurslar/', course_views.course_list_view, name='courses'),

    # --- KURS DETAY, KAYIT VE DERS İZLEME ---
    path('kurs/<slug:slug>/', course_views.course_detail_view, name='course_detail'),
    path('kurs/<slug:slug>/kayit/', course_views.enroll_course_view, name='enroll_course'),
    path('kurs/<slug:slug>/yorum-yap/', course_views.add_review_view, name='add_review'),
    path('kurs/<slug:course_slug>/ders/<int:lesson_id>/', lesson_views.lesson_detail_view, name='lesson_detail'),

    # --- KİMLİK DOĞRULAMA ---
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),

    # --- ŞİFRE SIFIRLAMA URL'LERİ ---
    path('sifremi-unuttum/', django_auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('sifremi-unuttum/gonderildi/', django_auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('sifre-sifirla/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('sifre-sifirla/tamamlandi/', django_auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    # --- KULLANICI / ÖĞRENCİ İŞLEMLERİ ---
    path('profil/', profile_views.profile_view, name='profile'),
    path('profil/egitmen-basvurusu/', profile_views.apply_instructor_view, name='apply_instructor'), # Senin eklediğin başvuru URL'i

    # --- EĞİTMEN PANELİ ---
    path('panel/', instructor_views.dashboard_view, name='dashboard'),
    path('panel/kurs-ekle/', instructor_views.add_course_view, name='add_course'),

    # --- SİSTEM YÖNETİMİ VE ONAY PANELİ ---
    path('sistem-yonetimi/', instructor_views.admin_dashboard_view, name='admin_dashboard'),
    path('sistem-yonetimi/basvuru-onayla/<int:app_id>/<str:action>/', instructor_views.approve_application_view, name='approve_application'),
    path('sistem-yonetimi/kurs-onayla/<int:course_id>/<str:action>/', instructor_views.approve_course_view, name='approve_course'),
]