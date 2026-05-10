from django.db.models import Q
from lms_app.models.users import Connection, Friendship, Message, CustomUser

def get_user_following(user):
    """Kullanıcının takip ettiği kişileri getirir."""
    return Connection.objects.filter(follower=user).select_related('following')

def get_user_followers(user):
    """Kullanıcıyı takip eden kişileri getirir."""
    return Connection.objects.filter(following=user).select_related('follower')

def get_user_friends(user):
    """Kullanıcının karşılıklı arkadaş olduğu kişileri liste olarak döner."""
    friendships = Friendship.objects.filter(
        (Q(from_user=user) | Q(to_user=user)),
        is_accepted=True
    ).select_related('from_user', 'to_user')

    friend_list = []
    for f in friendships:
        if f.from_user == user:
            friend_list.append(f.to_user)
        else:
            friend_list.append(f.from_user)
    return friend_list

def check_connection_exists(follower, following):
    """İki kullanıcı arasında takip ilişkisi olup olmadığını kontrol eder."""
    if not follower.is_authenticated:
        return False
    return Connection.objects.filter(follower=follower, following=following).exists()

def get_user_conversations(user):
    """Kullanıcının yaptığı son görüşmeleri listeler."""
    all_messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')

    conversations = []
    seen_users = set()

    for msg in all_messages:
        other_user = msg.receiver if msg.sender == user else msg.sender
        if other_user not in seen_users:
            seen_users.add(other_user)
            conversations.append({
                'user': other_user,
                'last_message': msg,
            })
    return conversations

def get_chat_history(user1, user2):
    """İki kullanıcı arasındaki mesaj geçmişini getirir."""
    return Message.objects.filter(
        Q(sender=user1, receiver=user2) |
        Q(sender=user2, receiver=user1)
    ).order_by('created_at')

def search_public_users(query, exclude_user_id):
    """Gizli olmayan kullanıcılar arasında arama yapar."""
    if not query:
        return []
    return CustomUser.objects.filter(
        username__icontains=query,
        is_private=False
    ).exclude(id=exclude_user_id)