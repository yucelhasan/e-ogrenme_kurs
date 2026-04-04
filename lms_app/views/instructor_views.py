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
        # Resim yükleme işlemi olacağı için request.FILES parametresi
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Formu hemen kaydetme, önce eğitmeni (instructor) ata
            course = form.save(commit=False)
            course.instructor = request.user 
            course.save()
            messages.success(request, "Kursunuz başarıyla oluşturuldu!")
            return redirect('dashboard')
    else:
        form = CourseForm()

    return render(request, 'admin_panel/add_course.html', {'form': form})