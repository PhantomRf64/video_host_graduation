from django import forms
from .models import VideoItem


class CraateVideo_Form(forms.ModelForm):

    class Meta:
        model = VideoItem
        fields = "__all__"
