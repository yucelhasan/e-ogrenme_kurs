# lms_app/views/course_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.selectors.course_selectors import get_active_courses, get_course_detail
from lms_app.models import Course, Enrollment
from lms_app.services.enrollment_services import enroll_user_to_course

def home_view(request):
    courses = get_active_courses()
    return render(request, 'home.html', {'courses': courses})


def course_list_view(request):
    search_query = request.GET.get('q', '')
    courses = get_active_courses(search_query=search_query)
    return render(request, 'courses/list.html', {
        'courses': courses,
        'search_query': search_query
    })


def course_detail_view(request, slug):
    course = get_course_detail(slug)

    return render(request, 'courses/detail.html', {'course': course})

@login_required
def enroll_course_view(request, slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug, is_active=True)

        # 1. Adımda yazdığımız servisi çağırıyoruz!
        success, message = enroll_user_to_course(request.user, course)

        # Servisten gelen sonuca göre ekrana yeşil veya sarı mesaj bas
        if success:
            messages.success(request, message)
        else:
            messages.warning(request, message)

    # İşlem bitince kullanıcıyı tekrar aynı kurs detay sayfasına fırlat
    return redirect('course_detail', slug=slug)