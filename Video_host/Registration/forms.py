from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from . import models


class Registration_Form(UserCreationForm):
    class Meta:
        model = models.MyUser
        fields = ("username", "password1", "password2")

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Имя пользователя"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""    

        self.fields["username"].widget.attrs.update({
            "placeholder": "Введите имя пользователя"
            })
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Введите пароль"
            })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Повторите пароль"
            })

class Login_Form(AuthenticationForm):
    pass


