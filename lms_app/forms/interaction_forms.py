from django import forms
from lms_app.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            # Yıldızlar için HTML tarafında özel tasarım (CSS/JS) yapacağımız için 
            # buraya ekstra class eklemiyoruz ama backend doğrulaması form üzerinden geçecek.
            'rating': forms.NumberInput(attrs={'style': 'display:none;'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Kurs hakkındaki düşüncelerinizi buraya yazın...',
                'required': True
            }),
        }