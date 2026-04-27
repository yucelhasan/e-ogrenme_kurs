from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.auth_forms import UserUpdateForm, InstructorApplicationForm
from lms_app.selectors.progress_selectors import get_user_enrolled_courses_with_progress
from lms_app.models import InstructorApplication, Certificate, CustomUser


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
    certificates = Certificate.objects.filter(student=request.user).select_related('course')

    return render(request, 'profile.html', {
        'form': form,
        'enrollments': enrollments,
        'completed_count': completed_count,
        'certificates': certificates
    })


@login_required
def apply_instructor_view(request):
    if request.user.role in ['instructor', 'admin']:
        messages.info(request, "Zaten eğitmen yetkisine sahipsiniz.")
        return redirect('profile')

    existing_application = InstructorApplication.objects.filter(user=request.user, status='pending').exists()
    if existing_application:
        messages.warning(request, "Zaten değerlendirmede olan bir başvurunuz bulunuyor. Lütfen onaylanmasını bekleyin.")
        return redirect('profile')

    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request,
                             "Harika! Eğitmenlik başvurunuz alındı. Yöneticilerimiz en kısa sürede inceleyecektir.")
            return redirect('profile')
    else:
        form = InstructorApplicationForm()

    return render(request, 'auth/apply_instructor.html', {'form': form})


# YENİ EKLENEN: PUBLIC PROFİL GÖRÜNTÜLEME
@login_required
def public_profile_view(request, username):
    target_user = get_object_or_404(CustomUser, username=username)

    # 1. KURAL: Admin anonimliği
    if target_user.role == 'admin':
        return render(request, 'profile_public.html', {
            'is_admin': True,
            'message': 'Bu profil sistem yöneticisine aittir. Kişisel bilgiler gizlenmiştir.'
        })

    # 2. KURAL: Kullanıcı profilini gizlediyse
    if target_user.is_private and target_user != request.user:
        return render(request, 'profile_public.html', {
            'is_private': True,
            'message': 'Bu kullanıcı profilini gizli olarak ayarlamıştır.',
            'target_user': target_user
        })

    # 3. KURAL: Normal görünüm (Açık profil)
    return render(request, 'profile_public.html', {
        'is_admin': False,
        'is_private': False,
        'target_user': target_user
    })