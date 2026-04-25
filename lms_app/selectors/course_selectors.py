from django.db.models import Q
from django.shortcuts import get_object_or_404
from lms_app.models import Course, Category

def get_all_categories():
    """Formdaki dropdown için tüm aktif kategorileri çeker."""
    return Category.objects.filter(is_active=True)

def get_active_courses(search_query=None, category_slug=None, min_price=None, max_price=None, sort_by=None):
    """
    Ana sayfa ve kurs listesi için sadece 'Yayınlandı' durumundaki kursları filtreler ve sıralar.
    """
    # DİKKAT: Artık is_active=True yerine status='published' kullanıyoruz.
    queryset = Course.objects.filter(status='published').select_related('category', 'instructor')

    # 1. Kelime ile Arama
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # 2. Kategori Filtresi
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    # 3. Minimum Fiyat Filtresi
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)

    # 4. Maksimum Fiyat Filtresi
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    # 5. Sıralama (Order By)
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price', '-created_at')  # Önce ucuzlar
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price', '-created_at')  # Önce pahalılar
    else:
        queryset = queryset.order_by('-created_at')  # Varsayılan: En yeniler

    return queryset

def get_course_detail(slug):
    """
    Kurs detay sayfasında kursu, modüllerini ve derslerini optimize edilmiş şekilde getirir.
    N+1 problemini çözmek için prefetch_related kullanılmıştır.
    """
    queryset = Course.objects.select_related('category', 'instructor').prefetch_related(
        'modules', 'modules__lessons'
    )
    return get_object_or_404(queryset, slug=slug, status='published')