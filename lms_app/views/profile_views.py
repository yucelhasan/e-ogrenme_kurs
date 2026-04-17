from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.auth_forms import UserUpdateForm
from lms_app.selectors.progress_selectors import get_user_enrolled_courses_with_progress

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