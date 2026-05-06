from lms_app.models.users import Connection, Message
from lms_app.services.system_services import create_log


def toggle_user_follow(request, target_user):
    """Kullanıcıyı takip eder veya takibi bırakır."""
    conn, created = Connection.objects.get_or_create(follower=request.user, following=target_user)

    if created:
        create_log(request, "Kullanıcı Takibi",
                   f"{request.user.username}, '{target_user.username}' kullanıcısını takip etmeye başladı.")
        return True, f"{target_user.username} kullanıcısını takip etmeye başladınız."
    else:
        conn.delete()
        create_log(request, "Takipten Çıkarma",
                   f"{request.user.username}, '{target_user.username}' kullanıcısını takipten çıkardı.")
        return False, "Takibi bıraktınız."


def send_message(request, receiver, content, log_action="Mesaj Gönderimi"):
    """Kullanıcılar arası mesaj oluşturur ve loglar."""
    message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
    create_log(request, log_action, f"{request.user.username}, '{receiver.username}' kullanıcısına mesaj gönderdi.")
    return message