from django import forms
from django.contrib.auth.forms import UserCreationForm
from lms_app.models import CustomUser, InstructorApplication

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Adınız", required=True)
    last_name = forms.CharField(max_length=30, label="Soyadınız", required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "phone")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'profile_picture', 'is_private'] # is_private EKLENDİ
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_private': 'Profilimi Gizli Yap (Sadece takipçilerim görebilir)',
        }

class InstructorApplicationForm(forms.ModelForm):
    class Meta:
        model = InstructorApplication
        fields = ['expertise']
        widgets = {
            'expertise': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tecrübelerinizden bahsedin...'
            })
        }