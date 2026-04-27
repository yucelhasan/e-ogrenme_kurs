from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.course_forms import CourseForm, ModuleForm, LessonForm
from lms_app.models import Course, InstructorApplication, Module, Lesson


# ==========================================
# 1. EĞİTMEN PANELİ (SADECE EĞİTMENLER İÇİN)
# ==========================================
@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')  # Admin yanlışlıkla buraya gelirse kendi paneline yolla

    if request.user.role != 'instructor':
        messages.error(request, "Bu panele erişim yetkiniz bulunmamaktadır.")
        return redirect('home')

    my_courses = Course.objects.filter(instructor=request.user).order_by('-created_at')
    return render(request, 'admin_panel/dashboard.html', {'my_courses': my_courses})


@login_required
def add_course_view(request):
    if request.user.role != 'instructor':
        messages.error(request, "Sadece eğitmenler kurs ekleyebilir.")
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES) # user=request.user parametresini formdan sildiysen burayı da sadeleştir
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.status = 'draft'  # Kursu 'Taslak' olarak başlatıyoruz
            course.save()
            messages.success(request, "Kurs taslağı oluşturuldu. Şimdi bölümleri ve dersleri ekleyebilirsiniz!")
            # Kullanıcıyı direkt müfredat yönetimi sayfasına yönlendiriyoruz
            return redirect('manage_curriculum', course_id=course.id)
    else:
        form = CourseForm()

    return render(request, 'admin_panel/add_course.html', {'form': form})

# ==========================================
# 2. ADMİN ONAY PANELİ (SADECE ADMİNLER İÇİN)
# ==========================================
@login_required
def admin_dashboard_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Bu sayfa sadece Sistem Yöneticileri içindir.")
        return redirect('home')

    pending_applications = InstructorApplication.objects.filter(status='pending').order_by('applied_at')
    pending_courses = Course.objects.filter(status='pending').order_by('created_at')

    return render(request, 'admin_panel/admin_dashboard.html', {
        'pending_applications': pending_applications,
        'pending_courses': pending_courses
    })


@login_required
def approve_application_view(request, app_id, action):
    if request.user.role != 'admin': return redirect('home')

    application = get_object_or_404(InstructorApplication, id=app_id)
    if action == 'approve':
        application.status = 'approved'
        application.user.role = 'instructor'  # Kullanıcının rolünü Eğitmen yap!
        application.user.save()
        messages.success(request, f"{application.user.username} artık bir Eğitmen!")
    elif action == 'reject':
        application.status = 'rejected'
        messages.warning(request, "Eğitmenlik başvurusu reddedildi.")

    application.save()
    return redirect('admin_dashboard')


@login_required
def approve_course_view(request, course_id, action):
    if request.user.role != 'admin': return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    if action == 'approve':
        course.status = 'published'  # Kursu yayına al!
        messages.success(request, f"'{course.title}' adlı kurs yayına alındı ve öğrencilere açıldı.")
    elif action == 'reject':
        course.status = 'rejected'
        messages.warning(request, "Kurs yayın başvurusu reddedildi.")

    course.save()
    return redirect('admin_dashboard')


@login_required
def manage_curriculum_view(request, course_id):
    # Sadece kendi kursuysa görebilir
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    return render(request, 'admin_panel/manage_curriculum.html', {
        'course': course,
        'module_form': ModuleForm(),
        'lesson_form': LessonForm()
    })


@login_required
def add_module_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, "Bölüm başarıyla eklendi!")
    return redirect('manage_curriculum', course_id=course.id)


@login_required
def add_lesson_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, "Ders başarıyla eklendi!")
    return redirect('manage_curriculum', course_id=module.course.id)


@login_required
def submit_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    # Kural: İçinde hiç modül yoksa onaya gönderilemez!
    if not course.modules.exists():
        messages.error(request, "Admin onayına göndermek için en az 1 Bölüm ve Ders eklemelisiniz.")
        return redirect('manage_curriculum', course_id=course.id)

    course.status = 'pending'
    course.save()
    messages.success(request, "Kursunuz başarıyla Admin onayına gönderildi. Teşekkürler!")
    return redirect('dashboard')