from django import forms
from lms_app.models import Course, CustomUser


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # instructor alanını listeye ekledik
        fields = ['title', 'category', 'instructor', 'description', 'price', 'image', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kursun Adı'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),  # Yeni widget
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Kurs detaylarını anlatın...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        # View'dan gönderdiğimiz 'user' bilgisini alıyoruz
        user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

        # Sadece 'instructor' rolündeki kullanıcıları seçilebilir yap
        self.fields['instructor'].queryset = CustomUser.objects.filter(role='instructor')

        # Eğer kullanıcı Admin DEĞİLSE, eğitmen seçimini gizle veya sadece kendini seçtir
        if user and user.role != 'admin':
            self.fields['instructor'].initial = user.id
            self.fields['instructor'].widget = forms.HiddenInput()  # Eğitmense bu alanı görmesin