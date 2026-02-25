from django import forms
from .models import VideoItem

class CreateVideo_Form(forms.ModelForm):
    class Meta:
        model = VideoItem
        fields = ['title', 'description', 'video', 'preview']

       
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название видео', 
                'style': 'background-color: #1a273b; color: #e0e0e0; border: 1px solid #607080;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание видео',
                'rows': 5,
                'style': 'background-color: #1a273b; color: #e0e0e0; border: 1px solid #607080;'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #1a273b; color: #e0e0e0;'
            }),
            'preview': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'background-color: #1a273b; color: #e0e0e0;'
            }),
        }