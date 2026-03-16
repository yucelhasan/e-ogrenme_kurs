from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms_app.urls')), # Ana sayfayı senin uygulamana yönlendirir
]