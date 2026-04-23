from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import Course, Enrollment, Review
from lms_app.forms.interaction_forms import ReviewForm
from lms_app.services.enrollment_services import enroll_user_to_course
from lms_app.selectors.course_selectors import get_active_courses, get_course_detail, get_all_categories

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
    
    # Kullanıcının kursa kayıtlı olup olmadığını kontrol et
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    # Kursa ait yorumları çek
    reviews = Review.objects.filter(course=course).select_related('student').order_by('-id')
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
        course = get_object_or_404(Course, slug=slug, is_active=True)
        success, message = enroll_user_to_course(request.user, course)
        if success:
            messages.success(request, message)
        else:
            messages.warning(request, message)
    return redirect('course_detail', slug=slug)

@login_required
def add_review_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)

    # 1. KURAL: Kullanıcı bu kursa kayıtlı mı?
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, "Bu kursa yorum yapabilmek için kayıt olmalısınız.")
        return redirect('course_detail', slug=slug)

    # 2. KURAL: Daha önce yorum yapmış mı?
    if Review.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "Bu kursa zaten bir değerlendirme yaptınız.")
        return redirect('course_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.student = request.user
            review.save()
            messages.success(request, "Değerlendirmeleriniz başarıyla eklendi, teşekkür ederiz!")
        else:
            messages.error(request, "Lütfen yıldız seçtiğinizden ve yorum yazdığınızdan emin olun.")

    return redirect('course_detail', slug=slug)

def course_list_view(request):
    # 1. URL'den gelen değerleri yakala
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price_str = request.GET.get('min_price', '')
    max_price_str = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'newest')

    # 2. Fiyat string'lerini (metin) güvenli bir şekilde sayıya (float) çevir
    try:
        min_price = float(min_price_str) if min_price_str else None
    except ValueError:
        min_price = None

    try:
        max_price = float(max_price_str) if max_price_str else None
    except ValueError:
        max_price = None

    # 3. Selector'a değerleri yolla ve filtrelenmiş veriyi al
    courses = get_active_courses(
        search_query=search_query,
        category_slug=category_slug,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

    # 4. Formdaki seçenekler için kategorileri çek
    categories = get_all_categories()

    # 5. HTML'e tüm değerleri geri gönder (Kullanıcı formu gönderdiğinde seçtiği değerler kaybolmasın diye)
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'min_price': min_price_str,
        'max_price': max_price_str,
        'sort_by': sort_by
    })