from lms_app.services.system_services import create_log
from django.utils.text import slugify
from lms_app.models import Category

def process_add_review(request, course, form):
    """Formdan gelen yorumu kaydeder ve sistem logunu oluşturur."""
    review = form.save(commit=False)
    review.course = course
    review.student = request.user
    review.save()

    create_log(request, "Kurs Değerlendirmesi",
               f"{request.user.username}, '{course.title}' kursuna yorum ve puan bıraktı.")

    return review

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
        # Yeni kategori talebi varsa oluştur
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

def create_question(user, lesson, form):
    """Ders altında yeni bir soru oluşturur."""
    question = form.save(commit=False)
    question.lesson = lesson
    question.student = user
    question.save()
    return question

def create_answer(user, question, form):
    """Bir soruya yeni bir cevap oluşturur."""
    answer = form.save(commit=False)
    answer.question = question
    answer.user = user
    answer.save()
    return answer