from django import forms
from lms_app.models.system import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duyuru Başlığı'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Duyuru içeriğini buraya yazın...'}),
        }
        labels = {
            'title': 'Başlık',
            'content': 'Duyuru İçeriği'
        }