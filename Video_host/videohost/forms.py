from django import forms
from .models import VideoItem

class CreateVideo_Form(forms.ModelForm):
    class Meta:
        model = VideoItem
        fields = ['title', 'description', 'video', 'preview']

        