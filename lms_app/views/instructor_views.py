from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lms_app.forms.course_forms import CourseForm
from lms_app.models import Course

@login_required
def dashboard_view(request):
    # Sadece Eğitmen ve Adminlerin erişmesine izin ver
    if request.user.role not in ['instructor', 'admin']:
        messages.error(request, "Bu panele erişim yetkiniz bulunmamaktadır.")
        return redirect('home')
        
    # Sadece bu eğitmenin kendi eklediği kursları getir
    my_courses = Course.objects.filter(instructor=request.user).order_by('-created_at')
    
    return render(request, 'admin_panel/dashboard.html', {'my_courses': my_courses})


@login_required
def add_course_view(request):
    if request.user.role not in ['instructor', 'admin']:
        messages.error(request, "Kurs ekleme yetkiniz yok.")
        return redirect('home')

    if request.method == 'POST':
        # Formu oluştururken user=request.user parametresini ekledik
        form = CourseForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            course = form.save(commit=False)

            # Eğer kullanıcı Admin ise, formdan gelen eğitmeni kullan
            # Değilse, kursun eğitmeni bizzat kendisidir
            if request.user.role != 'admin':
                course.instructor = request.user

            course.save()
            messages.success(request, "Kurs başarıyla oluşturuldu!")
            return redirect('dashboard')
    else:
        # GET isteğinde de user parametresini gönderiyoruz
        form = CourseForm(user=request.user)

    return render(request, 'admin_panel/add_course.html', {'form': form})