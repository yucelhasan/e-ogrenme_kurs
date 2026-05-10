from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.auth_forms import UserUpdateForm, InstructorApplicationForm
from lms_app.selectors.user_selectors import get_user_by_username, check_pending_instructor_application
from lms_app.selectors.progress_selectors import get_user_enrolled_courses_with_progress
from lms_app.selectors.system_selectors import get_student_certificates
from lms_app.selectors.social_selectors import get_user_following, get_user_followers, get_user_friends, check_connection_exists
from lms_app.services.user_services import update_user_profile, submit_instructor_application
from lms_app.services.badge_services import get_user_badges

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            update_user_profile(request, form)
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    enrollments = get_user_enrolled_courses_with_progress(request.user)
    completed_count = sum(1 for e in enrollments if e['progress'] == 100)
    certificates = get_student_certificates(request.user)

    following_conns = get_user_following(request.user)
    follower_conns = get_user_followers(request.user)
    friends = get_user_friends(request.user)
    my_badges = get_user_badges(request.user)

    return render(request, 'profile.html', {
        'form': form,
        'enrollments': enrollments,
        'completed_count': completed_count,
        'certificates': certificates,
        'following_conns': following_conns,
        'follower_conns': follower_conns,
        'friends': friends,
        'my_badges': my_badges,
    })


@login_required
def apply_instructor_view(request):
    if request.user.role in ['instructor', 'admin']:
        messages.info(request, "Zaten eğitmen yetkisine sahipsiniz.")
        return redirect('profile')

    if check_pending_instructor_application(request.user):
        messages.warning(request, "Zaten değerlendirmede olan bir başvurunuz bulunuyor.")
        return redirect('profile')

    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST)
        if form.is_valid():
            submit_instructor_application(request, form)
            messages.success(request, "Harika! Eğitmenlik başvurunuz alındı.")
            return redirect('profile')
    else:
        form = InstructorApplicationForm()

    return render(request, 'auth/apply_instructor.html', {'form': form})


@login_required
def public_profile_view(request, username):
    target_user = get_user_by_username(username)
    is_following = check_connection_exists(request.user, target_user)

    if target_user.role == 'admin':
        return render(request, 'profile_public.html', {
            'is_admin': True,
            'message': 'Sistem yöneticisi profili gizlidir.',
            'target_user': target_user
        })

    if target_user.is_private and target_user != request.user and not is_following:
        return render(request, 'profile_public.html', {
            'is_private': True,
            'message': 'Bu profil gizlidir. Görmek için takip etmelisiniz.',
            'target_user': target_user,
            'is_following': is_following
        })

    target_badges = get_user_badges(target_user)

    return render(request, 'profile_public.html', {
        'is_admin': False,
        'is_private': False,
        'target_user': target_user,
        'is_following': is_following,
        'target_badges': target_badges,
    })