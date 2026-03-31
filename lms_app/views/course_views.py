from django.shortcuts import render
from lms_app.selectors.course_selectors import get_active_courses

def home_view(request):
    # Veriyi veritabanından değil, Selector katmanından istiyoruz!
    courses = get_active_courses()
    return render(request, 'home.html', {'courses': courses})