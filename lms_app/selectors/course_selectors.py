from django.db.models import Q
from django.shortcuts import get_object_or_404
from lms_app.models import Course


def get_active_courses(search_query=None):
    """
    Ana sayfa ve kurs listesi için aktif kursları getirir.
    Arama sorgusu varsa filtreleme yapar.
    """
    queryset = Course.objects.filter(is_active=True).select_related('category', 'instructor').order_by('-created_at')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return queryset


def get_course_detail(slug):
    """
    Kurs detay sayfasında kursu, modüllerini ve derslerini optimize edilmiş şekilde getirir.
    N+1 problemini çözmek için prefetch_related kullanılmıştır.
    """
    # select_related: Tekil ilişkiler (Kategori, Eğitmen) için kullanılır (SQL JOIN yapar).
    # prefetch_related: Çoğul ilişkiler (Modüller ve Dersler) için kullanılır.

    queryset = Course.objects.select_related('category', 'instructor').prefetch_related(
        'modules',  # Kursa ait tüm modülleri tek seferde çek
        'modules__lessons'  # O modüllere ait tüm dersleri tek seferde çek
    )

    # Eğer kurs veritabanında varsa getir, yoksa (veya is_active=False ise) otomatik 404 Hata Sayfası fırlat
    return get_object_or_404(queryset, slug=slug, is_active=True)