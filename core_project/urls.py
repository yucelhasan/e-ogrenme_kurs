from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms_app.urls')),
]

# Hata sayfaları yönlendirmeleri
handler400 = 'lms_app.views.error_views.custom_400_view'
handler403 = 'lms_app.views.error_views.custom_403_view'
handler404 = 'lms_app.views.error_views.custom_404_view'
handler500 = 'lms_app.views.error_views.custom_500_view'