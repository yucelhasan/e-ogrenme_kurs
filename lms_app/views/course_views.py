from django.shortcuts import render
from lms_app.selectors.course_selectors import get_active_courses

def home_view(request):
    # Veriyi veritabanından değil, Selector katmanından istiyoruz!
    courses = get_active_courses()
    return render(request, 'home.html', {'courses': courses})

def course_list_view(request):
    # Kullanıcının arama çubuğuna yazdığı 'q' parametresini al
    search_query = request.GET.get('q', '')
    
    # Kelimeyi veritabanı sorgusuna gönder
    courses = get_active_courses(search_query=search_query) 
    
    return render(request, 'courses/list.html', {
        'courses': courses,
        'search_query': search_query # Arama kutusunun içinde kullanıcının yazdığı kelimeyi tekrar göstermek için
    })