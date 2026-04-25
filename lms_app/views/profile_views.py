from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.auth_forms import UserUpdateForm, InstructorApplicationForm
from lms_app.selectors.progress_selectors import get_user_enrolled_courses_with_progress
from lms_app.models import InstructorApplication

@login_required
def profile_view(request):
    if request.method == 'POST':
        # request.FILES: Resim yükleme işlemleri için GEREKLİDİR
        # instance=request.user: Mevcut kullanıcının bilgilerinin formda dolu gelmesini sağlar
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    enrollments = get_user_enrolled_courses_with_progress(request.user)

    completed_count = sum(1 for e in enrollments if e['progress'] == 100)

    return render(request, 'profile.html', {
        'form': form,
        'enrollments': enrollments,
        'completed_count': completed_count
    })

@login_required
def apply_instructor_view(request):
    # 1. KONTROL: Zaten eğitmen veya adminse engelle
    if request.user.role in ['instructor', 'admin']:
        messages.info(request, "Zaten eğitmen yetkisine sahipsiniz.")
        return redirect('profile')

    # 2. KONTROL: Bekleyen bir başvurusu varsa engelle
    existing_application = InstructorApplication.objects.filter(user=request.user, status='pending').exists()
    if existing_application:
        messages.warning(request, "Zaten değerlendirmede olan bir başvurunuz bulunuyor. Lütfen onaylanmasını bekleyin.")
        return redirect('profile')

    # 3. Form İşlemleri
    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user # Başvuruyu yapan kullanıcıyı ata
            application.save()
            messages.success(request, "Harika! Eğitmenlik başvurunuz alındı. Yöneticilerimiz en kısa sürede inceleyecektir.")
            return redirect('profile')
    else:
        form = InstructorApplicationForm()

    return render(request, 'auth/apply_instructor.html', {'form': form})