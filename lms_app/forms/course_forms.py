from django import forms
from lms_app.models import Course, Module, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'new_category_request', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kursun Adı'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'new_category_request': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Örn: Yapay Zeka, Müzik Prodüksiyonu...'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Kurs detaylarını anlatın...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # View'dan gönderilen 'user' bilgisini yakalayıp formdan koparıyoruz ki Django hata vermesin
        kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category_request')

        # KURAL 1: Eğitmen ne bir kategori seçmiş ne de yeni bir tane yazmışsa hata ver.
        if not category and not new_category:
            raise forms.ValidationError(
                "Lütfen listeden bir kategori seçin veya bulamadıysanız yeni bir kategori önerin.")

        # KURAL 2: Eğitmen hem listeden kategori seçmiş hem de yeni kategori yazmışsa, listedekini baz al ve yazdığını temizle.
        if category and new_category:
            cleaned_data['new_category_request'] = None

        return cleaned_data


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Örn: Bölüm 1: Python'a Giriş"}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'duration']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Örn: Değişkenler ve Veri Tipleri'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dersin metin içeriği veya açıklaması...'}),
            'video_url': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 10:45'}),
        }