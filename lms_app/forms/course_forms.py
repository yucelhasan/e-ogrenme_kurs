from django import forms
from lms_app.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kursun Adı'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Kurs detaylarını anlatın...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # View'dan gönderilen 'user' bilgisini yakalayıp formdan koparıyoruz ki Django hata vermesin
        kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

        # DİKKAT: Eski self.fields['instructor'] ayarlarının TAMAMINI sildik!