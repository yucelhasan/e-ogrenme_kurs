from django import forms
from django.contrib.auth.forms import UserCreationForm
from lms_app.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Adınız", required=True)
    last_name = forms.CharField(max_length=30, label="Soyadınız", required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "phone", "role")

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