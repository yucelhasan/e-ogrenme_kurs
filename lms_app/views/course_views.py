# lms_app/views/course_views.py
from django.shortcuts import render
from lms_app.selectors.course_selectors import get_active_courses, get_course_detail


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