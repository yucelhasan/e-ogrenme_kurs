from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.models.users import CustomUser
from lms_app.selectors.user_selectors import get_user_by_username
from lms_app.selectors.social_selectors import get_user_conversations, get_chat_history, search_public_users
from lms_app.services.social_services import toggle_user_follow, send_message


@login_required
def inbox_view(request):
    conversations = get_user_conversations(request.user)
    return render(request, 'social/inbox.html', {'conversations': conversations})


@login_required
def follow_user_view(request, username):
    target_user = get_user_by_username(username)

    if target_user == request.user:
        return redirect('public_profile', username=username)

    is_following, message = toggle_user_follow(request, target_user)

    if is_following:
        messages.success(request, message)
    else:
        messages.info(request, message)

    return redirect('public_profile', username=username)


@login_required
def send_message_view(request, username):
    receiver = get_user_by_username(username)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            send_message(request, receiver, content)
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
            send_message(request, receiver, content, log_action="Direkt Mesaj")
            messages.success(request, f"Mesajınız '{target_username}' adlı kullanıcıya başarıyla ulaştı.")
        else:
            messages.error(request, f"'{target_username}' adında bir kullanıcı bulunamadı.")

    return redirect('inbox')


@login_required
def search_users_view(request):
    query = request.GET.get('q', '')
    users = search_public_users(query, request.user.id)
    return render(request, 'social/search_users.html', {'users': users, 'query': query})


@login_required
def chat_view(request, username):
    other_user = get_user_by_username(username)
    chat_messages = get_chat_history(request.user, other_user)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content and content.strip():
            send_message(request, other_user, content, log_action="Sohbet İçi Mesaj")
            return redirect('chat', username=username)

    return render(request, 'social/chat.html', {
        'other_user': other_user,
        'chat_messages': chat_messages
    })