from django import forms
from lms_app.models import Course, Module, Lesson
from django.utils.text import slugify


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

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title:
            slug = slugify(title)

            existing_courses = Course.objects.filter(slug=slug)

            if self.instance and self.instance.pk:
                existing_courses = existing_courses.exclude(pk=self.instance.pk)

            if existing_courses.exists():
                raise forms.ValidationError(
                    "Bu başlığa sahip bir kurs zaten sistemde mevcut. Lütfen farklı bir başlık belirleyiniz.")

        return title

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category_request')

        if not category and not new_category:
            raise forms.ValidationError(
                "Lütfen listeden bir kategori seçin veya bulamadıysanız yeni bir kategori önerin.")

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