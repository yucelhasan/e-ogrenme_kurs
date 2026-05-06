from django import forms
from lms_app.models import Review, Question, Answer

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'style': 'display:none;'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Yorumunuz...'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sorunuzun başlığı...'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detaylı açıklama...'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Cevabınızı yazın...'}),
        }