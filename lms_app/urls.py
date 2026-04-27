from django.urls import path
from .views import (
    cart_views, auth_views, course_views,
    profile_views, instructor_views, lesson_views, social_views
)
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    # --- KURS VE ANA SAYFA İŞLEMLERİ ---
    path('', course_views.home_view, name='home'),
    path('kurslar/', course_views.course_list_view, name='courses'),
    path('kurs/<slug:slug>/', course_views.course_detail_view, name='course_detail'),
    path('kurs/<slug:slug>/kayit/', course_views.enroll_course_view, name='enroll_course'),
    path('kurs/<slug:slug>/yorum-yap/', course_views.add_review_view, name='add_review'),
    path('kurs/<slug:course_slug>/ders/<int:lesson_id>/', lesson_views.lesson_detail_view, name='lesson_detail'),

    # --- KİMLİK DOĞRULAMA İŞLEMLERİ ---
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('sifremi-unuttum/', django_auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('sifremi-unuttum/gonderildi/', django_auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('sifre-sifirla/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('sifre-sifirla/tamamlandi/', django_auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    # --- KULLANICI / SOSYAL / PROFİL İŞLEMLERİ ---
    path('profil/', profile_views.profile_view, name='profile'),
    path('profil/egitmen-basvurusu/', profile_views.apply_instructor_view, name='apply_instructor'),
    path('kullanici/<str:username>/', profile_views.public_profile_view, name='public_profile'),
    path('kullanici/<str:username>/takip/', social_views.follow_user_view, name='follow_user'),
    path('kullanici/<str:username>/mesaj-gonder/', social_views.send_message_view, name='send_message'),

    # --- DERS İÇİ SORU & CEVAP ---
    path('soru/<int:question_id>/cevapla/', lesson_views.add_answer_view, name='add_answer'),

    # --- EĞİTMEN PANELİ ---
    path('panel/', instructor_views.dashboard_view, name='dashboard'),
    path('panel/kurs-ekle/', instructor_views.add_course_view, name='add_course'),
    path('panel/kurs/<int:course_id>/mufredat/', instructor_views.manage_curriculum_view, name='manage_curriculum'),
    path('panel/kurs/<int:course_id>/modul-ekle/', instructor_views.add_module_view, name='add_module'),
    path('panel/modul/<int:module_id>/ders-ekle/', instructor_views.add_lesson_view, name='add_lesson'),
    path('panel/kurs/<int:course_id>/onaya-gonder/', instructor_views.submit_course_view, name='submit_course'),
    path('panel/kurs/<int:course_id>/arsivle/', instructor_views.archive_course_view, name='archive_course'),

    # --- SİSTEM YÖNETİMİ VE ONAY PANELİ (ADMİN) ---
    path('sistem-yonetimi/', instructor_views.admin_dashboard_view, name='admin_dashboard'),
    path('sistem-yonetimi/basvuru-onayla/<int:app_id>/<str:action>/', instructor_views.approve_application_view, name='approve_application'),
    path('sistem-yonetimi/kurs-onayla/<int:course_id>/<str:action>/', instructor_views.approve_course_view, name='approve_course'),

    # --- SEPET VE ÖDEME İŞLEMLERİ ---
    path('sepet/', cart_views.view_cart_view, name='view_cart'),
    path('sepet/ekle/<slug:slug>/', cart_views.add_to_cart_view, name='add_to_cart'),
    path('sepet/cikar/<int:item_id>/', cart_views.remove_from_cart_view, name='remove_from_cart'),
    path('sepet/odeme/', cart_views.checkout_view, name='checkout'),
]