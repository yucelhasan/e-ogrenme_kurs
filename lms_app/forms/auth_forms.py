from django import forms
from django.contrib.auth.forms import UserCreationForm
from lms_app.models import CustomUser, InstructorApplication

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Adınız", required=True)
    last_name = forms.CharField(max_length=30, label="Soyadınız", required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # DİKKAT: 'role' ve 'expertise' alanları çıkarıldı. Herkes 'student' olarak kaydedilecek.
        fields = ("username", "first_name", "last_name", "email", "phone")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadınız'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon Numaranız'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class InstructorApplicationForm(forms.ModelForm):
    class Meta:
        model = InstructorApplication
        fields = ['expertise']
        widgets = {
            'expertise': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Hangi alanlarda uzmansınız? Daha önce nerede eğitim verdiniz? Lütfen kısaca kendinizden bahsedin...'
            })
        }