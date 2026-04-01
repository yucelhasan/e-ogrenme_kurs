from django.db.models import Q
from lms_app.models import Course

def get_active_courses(search_query=None):
    """
    Ana sayfa ve kurs listesi için aktif kursları getirir.
    Arama sorgusu varsa filtreleme yapar.
    """
    queryset = Course.objects.filter(is_active=True).select_related('category', 'instructor').order_by('-created_at')
    
    # Eğer bir arama kelimesi gönderilmişse filtrele
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    return queryset