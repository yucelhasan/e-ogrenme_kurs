from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models import CustomUser, Connection, Message


@login_required
def inbox_view(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-created_at')
    messages_sent = Message.objects.filter(sender=request.user).order_by('-created_at')

    return render(request, 'social/inbox.html', {
        'messages_received': messages_received,
        'messages_sent': messages_sent
    })


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


# YENİ EKLENEN: Gelen kutusu içinden isimle direkt mesaj atma
@login_required
def send_message_direct_view(request):
    if request.method == 'POST':
        target_username = request.POST.get('username')
        content = request.POST.get('content')

        if target_username == request.user.username:
            messages.error(request, "Kendinize mesaj gönderemezsiniz.")
            return redirect('inbox')

        receiver = CustomUser.objects.filter(username=target_username).first()
        if receiver:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, f"Mesajınız '{target_username}' adlı kullanıcıya başarıyla ulaştı.")
        else:
            messages.error(request,
                           f"'{target_username}' adında bir kullanıcı bulunamadı. Lütfen kullanıcı adını doğru yazdığınızdan emin olun.")

    return redirect('inbox')