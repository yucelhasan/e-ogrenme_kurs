from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import CustomUser, Connection, Message


@login_required
def follow_user_view(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if target_user == request.user:
        return redirect('public_profile', username=username)

    conn, created = Connection.objects.get_or_create(follower=request.user, following=target_user)
    if created:
        messages.success(request, f"{target_user.username} kullanıcısını takip etmeye başladınız.")
    else:
        conn.delete()
        messages.info(request, "Takibi bıraktınız.")

    return redirect('public_profile', username=username)


@login_required
def send_message_view(request, username):
    receiver = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, "Mesajınız başarıyla gönderildi.")
    return redirect('public_profile', username=username)