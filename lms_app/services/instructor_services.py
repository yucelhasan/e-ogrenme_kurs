from django.utils.text import slugify
from lms_app.models import Category
from lms_app.services.system_services import create_log

def handle_instructor_application(app, action):
    """Eğitmenlik başvurusunu onaylar veya reddeder."""
    if action == 'approve':
        app.status = 'approved'
        app.user.role = 'instructor'
        app.user.save()
    else:
        app.status = 'rejected'
    app.save()

def handle_course_approval(request, course, action):
    """Kursu yayına alır veya reddeder."""
    if action == 'approve':
        if course.new_category_request:
            new_cat, _ = Category.objects.get_or_create(
                name=course.new_category_request,
                defaults={'slug': slugify(course.new_category_request)}
            )
            course.category = new_cat
            course.new_category_request = None

        course.status = 'published'
        course.save()
        create_log(request, "Kurs Onayı", f"Admin, '{course.title}' isimli kursu yayına aldı.")
        return True
    else:
        course.status = 'rejected'
        course.save()
        create_log(request, "Kurs Reddi", f"Admin, '{course.title}' isimli kursu reddetti.")
        return False

def delete_course_with_log(request, course):
    """Kursu siler ve logunu tutar."""
    title = course.title
    course.delete()
    create_log(request, "Kurs Silme", f"'{title}' isimli kurs ve tüm içeriği silindi.")
    return title