from django import forms
from lms_app.models.assessments import Quiz, Assignment
from lms_app.models.assessments import AssignmentSubmission

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['text_response', 'file']
        widgets = {
            'text_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ödev açıklamanız veya metin yanıtınız...'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'passing_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Bölüm 1 Sonu Değerlendirmesi'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control', 'value': 70}),
        }
        labels = {
            'title': 'Quiz Başlığı',
            'passing_score': 'Geçme Notu (0-100)'
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Bitirme Projesi Teslimi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Öğrencilerden ne beklediğinizi detaylıca yazın...'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Ödev Başlığı',
            'description': 'Ödev Yönergesi',
            'due_date': 'Son Teslim Tarihi'
        }

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'max': '100', 'min': '0', 'placeholder': '100 üzerinden not verin'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Öğrenciye geri bildiriminiz...'}),
        }
        labels = {
            'score': 'Verilen Not',
            'feedback': 'Geri Bildirim'
        }