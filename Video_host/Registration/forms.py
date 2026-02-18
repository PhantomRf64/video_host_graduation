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

        
        for field in self.fields.values():
            field.help_text = ""

       
        self.fields["username"].widget.attrs.update({
            "placeholder": "Введите имя пользователя",
            "class": "form-control"
        })
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Введите пароль",
            "class": "form-control"
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Повторите пароль",
            "class": "form-control"
        })


class Login_Form(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields["username"].widget.attrs.update({
            "placeholder": "Введите имя пользователя",
            "class": "form-control"
        })
        self.fields["password"].widget.attrs.update({
            "placeholder": "Введите пароль",
            "class": "form-control"
        })

        
        self.fields["username"].label = "Имя пользователя"
        self.fields["password"].label = "Пароль"
