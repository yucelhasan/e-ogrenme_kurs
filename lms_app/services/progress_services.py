from lms_app.models import LessonProgress

def mark_lesson_as_completed(user, lesson):
    progress, created = LessonProgress.objects.get_or_create(
        student=user,
        lesson=lesson,
        defaults={'is_completed': True}
    )

    if not created and not progress.is_completed:
        progress.is_completed = True
        progress.save()

    return progress