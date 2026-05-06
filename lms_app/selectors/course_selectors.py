from django.db.models import Q
from django.shortcuts import get_object_or_404
from lms_app.models import Course, Category, Lesson

def get_all_categories():
    """Formdaki dropdown için tüm aktif kategorileri çeker."""
    return Category.objects.filter(is_active=True)

def get_active_courses(search_query=None, category_slug=None, min_price=None, max_price=None, sort_by=None):
    """
    Ana sayfa ve kurs listesi için sadece 'Yayınlandı' durumundaki kursları filtreler ve sıralar.
    """
    queryset = Course.objects.filter(status='published').select_related('category', 'instructor')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)

    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    if sort_by == 'price_asc':
        queryset = queryset.order_by('price', '-created_at')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price', '-created_at')
    else:
        queryset = queryset.order_by('-created_at')

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

def get_instructor_published_course_count(instructor):
    from lms_app.models import Course
    if not instructor.is_authenticated:
        return 0
    return Course.objects.filter(instructor=instructor, status='published').count()

def get_published_course_by_slug(slug):
    """Sadece yayında olan kursu slug değerine göre getirir."""
    return get_object_or_404(Course, slug=slug, status='published')

def get_published_course_by_slug(slug):
    """Yayında olan bir kursu slug bilgisine göre getirir."""
    return get_object_or_404(Course, slug=slug, status='published')

def get_lesson_by_id_and_course(lesson_id, course):
    """Belirli bir kursa ait dersi ID bilgisine göre getirir."""
    return get_object_or_404(Lesson, id=lesson_id, module__course=course)