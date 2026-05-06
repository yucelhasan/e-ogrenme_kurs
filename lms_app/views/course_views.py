from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.interaction_forms import ReviewForm
from lms_app.selectors.course_selectors import get_active_courses, get_course_detail, get_all_categories, get_published_course_by_slug
from lms_app.selectors.enrollment_selectors import check_enrollment
from lms_app.selectors.interaction_selectors import get_course_reviews, check_user_reviewed_course
from lms_app.services.enrollment_services import enroll_user_to_course
from lms_app.services.system_services import create_log
from lms_app.services.interaction_services import process_add_review


def home_view(request):
    courses = get_active_courses()
    return render(request, 'home.html', {'courses': courses})


def course_detail_view(request, slug):
    course = get_course_detail(slug)

    is_enrolled = check_enrollment(request.user, course)

    reviews = get_course_reviews(course)
    review_form = ReviewForm()

    return render(request, 'courses/detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'reviews': reviews,
        'review_form': review_form
    })


@login_required
def enroll_course_view(request, slug):
    if request.method == 'POST':
        course = get_published_course_by_slug(slug)
        success, message = enroll_user_to_course(request.user, course)
        if success:
            create_log(request, "Direkt Kursa Kayıt",
                       f"{request.user.username}, '{course.title}' kursuna başarıyla kayıt oldu.")
            messages.success(request, message)
        else:
            messages.warning(request, message)
    return redirect('course_detail', slug=slug)


@login_required
def add_review_view(request, slug):
    course = get_published_course_by_slug(slug)

    if not check_enrollment(request.user, course):
        messages.error(request, "Bu kursa yorum yapabilmek için kayıt olmalısınız.")
        return redirect('course_detail', slug=slug)

    if check_user_reviewed_course(request.user, course):
        messages.warning(request, "Bu kursa zaten bir değerlendirme yaptınız.")
        return redirect('course_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            process_add_review(request, course, form)
            messages.success(request, "Değerlendirmeleriniz başarıyla eklendi, teşekkür ederiz!")
        else:
            messages.error(request, "Lütfen yıldız seçtiğinizden ve yorum yazdığınızdan emin olun.")

    return redirect('course_detail', slug=slug)


def course_list_view(request):
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price_str = request.GET.get('min_price', '')
    max_price_str = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'newest')

    try:
        min_price = float(min_price_str) if min_price_str else None
    except ValueError:
        min_price = None

    try:
        max_price = float(max_price_str) if max_price_str else None
    except ValueError:
        max_price = None

    courses = get_active_courses(
        search_query=search_query,
        category_slug=category_slug,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

    categories = get_all_categories()

    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'min_price': min_price_str,
        'max_price': max_price_str,
        'sort_by': sort_by
    })