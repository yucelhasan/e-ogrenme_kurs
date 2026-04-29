# lms_app/views/social_views.py

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from lms_app.models import CustomUser, Connection, Message
from lms_app.services.system_services import create_log  # YENİ: Log servisi eklendi


@login_required
def inbox_view(request):
    """Instagram DM kutusu mantığında mesajlaşılan kişileri listeler."""
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')

    conversations = []
    seen_users = set()

    for msg in all_messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user not in seen_users:
            seen_users.add(other_user)
            conversations.append({
                'user': other_user,
                'last_message': msg,
            })

    return render(request, 'social/inbox.html', {'conversations': conversations})


@login_required
def follow_user_view(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if target_user == request.user:
        return redirect('public_profile', username=username)

    conn, created = Connection.objects.get_or_create(follower=request.user, following=target_user)
    if created:
        # YENİ: Takip etme logu
        create_log(request, "Kullanıcı Takibi", f"{request.user.username}, '{target_user.username}' kullanıcısını takip etmeye başladı.")
        messages.success(request, f"{target_user.username} kullanıcısını takip etmeye başladınız.")
    else:
        conn.delete()
        # YENİ: Takipten çıkma logu
        create_log(request, "Takipten Çıkarma", f"{request.user.username}, '{target_user.username}' kullanıcısını takipten çıkardı.")
        messages.info(request, "Takibi bıraktınız.")

    return redirect('public_profile', username=username)


@login_required
def send_message_view(request, username):
    receiver = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            # YENİ: Profil üzerinden mesaj gönderme logu
            create_log(request, "Mesaj Gönderimi", f"{request.user.username}, '{receiver.username}' kullanıcısına profil üzerinden mesaj gönderdi.")
            messages.success(request, "Mesajınız başarıyla gönderildi.")
    return redirect('public_profile', username=username)


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
            # YENİ: Gelen kutusu üzerinden yeni mesaj logu
            create_log(request, "Direkt Mesaj", f"{request.user.username}, '{receiver.username}' kullanıcısına yeni bir mesaj gönderdi.")
            messages.success(request, f"Mesajınız '{target_username}' adlı kullanıcıya başarıyla ulaştı.")
        else:
            messages.error(request, f"'{target_username}' adında bir kullanıcı bulunamadı. Lütfen kullanıcı adını doğru yazdığınızdan emin olun.")

    return redirect('inbox')


@login_required
def search_users_view(request):
    """Kullanıcı adıyla arkadaş arama fonksiyonu"""
    query = request.GET.get('q', '')
    users = []

    if query:
        users = CustomUser.objects.filter(
            username__icontains=query,
            is_private=False
        ).exclude(id=request.user.id)

    return render(request, 'social/search_users.html', {'users': users, 'query': query})


@login_required
def chat_view(request, username):
    """İki kişi arasındaki sohbet (Chat) akışını sağlayan fonksiyon"""
    other_user = get_object_or_404(CustomUser, username=username)

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            create_log(request, "Sohbet İçi Mesaj", f"{request.user.username}, '{other_user.username}' kullanıcısına mesaj gönderdi.")
            return redirect('chat', username=username)

    return render(request, 'social/chat.html', {
        'other_user': other_user,
        'chat_messages': chat_messages
    })