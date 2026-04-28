from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from lms_app.models import CustomUser, Connection, Message


@login_required
def inbox_view(request):
    """Instagram DM kutusu mantığında mesajlaşılan kişileri listeler."""

    # Kullanıcının gönderdiği veya aldığı TÜM mesajları tarihe göre (en yeniden eskiye) çek
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')  # Modelindeki tarih alanının adına göre (örn: timestamp) değiştir

    conversations = []
    seen_users = set()

    # Mesajları tek tek dön ve her kullanıcıyla olan SADECE EN SON mesajı al
    for msg in all_messages:
        # Karşıdaki kişiyi bul (Eğer gönderen bensem alıcıdır, alıcı bensem gönderendir)
        other_user = msg.receiver if msg.sender == request.user else msg.sender

        # Eğer bu kullanıcıyı daha önce listeye eklemediysek ekle
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


@login_required
def search_users_view(request):
    """Kullanıcı adıyla arkadaş arama fonksiyonu"""
    query = request.GET.get('q', '')
    users = []

    if query:
        # Arama yapıldıysa: Kendi profili hariç, içinde aranan kelime geçenleri getir
        users = CustomUser.objects.filter(
            username__icontains=query,
            is_private=False  # Sadece gizli olmayan profilleri göster
        ).exclude(id=request.user.id)

    return render(request, 'social/search_users.html', {'users': users, 'query': query})


@login_required
def chat_view(request, username):
    """İki kişi arasındaki sohbet (Chat) akışını sağlayan fonksiyon"""
    other_user = get_object_or_404(CustomUser, username=username)

    # 1. İki kişi arasındaki TÜM mesajları (hem giden hem gelen) tarihe göre sırala
    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')  # 'timestamp' veya 'created_at' olarak ayarlayın

    # 2. Yeni mesaj gönderme işlemi (POST)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat', username=username)

    return render(request, 'social/chat.html', {
        'other_user': other_user,
        'chat_messages': chat_messages
    })