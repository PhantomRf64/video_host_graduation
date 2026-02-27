from django import forms
from .models import VideoItem

class CreateVideo_Form(forms.ModelForm):
    class Meta:
        model = VideoItem
        fields = ['title', 'description', 'video', 'preview']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Введите название видео'
            }),
            'description': forms.Textarea(attrs={
                'class': 'custom-textarea',
                'rows': 3,
                'placeholder': 'Краткое описание...'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'd-none',
                'id': 'videoInput'
            }),
            'preview': forms.ClearableFileInput(attrs={
                'class': 'd-none',
                'id': 'previewInput'
            }),
        }