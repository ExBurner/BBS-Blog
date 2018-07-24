from django import forms
from .models import *
from django.core.exceptions import ValidationError

wid_1 = forms.widgets.TextInput(attrs={"class": "form-control", "autocomplete": "off"})
wid_2 = forms.widgets.PasswordInput(attrs={"class": "form-control"})
required = {"required": "该字段不能为空！"}


class UserForm(forms.Form):
    username = forms.CharField(max_length=32, label="用户名", widget=wid_1,
                               error_messages={"required": "该字段不能为空！"})
    password = forms.CharField(min_length=8, label="密码", widget=wid_2,
                               error_messages={"min_length": "密码长度至少8位！",
                                               "required": "该字段不能为空！"})
    re_password = forms.CharField(min_length=8, label="确认密码", widget=wid_2,
                                  error_messages={"min_length": "密码长度至少8位！",
                                                  "required": "该字段不能为空！"})
    email = forms.EmailField(label="邮箱", widget=wid_1,
                             error_messages={"invalid": "邮箱格式错误！"})

    def clean_username(self):
        """
        判断注册时的用户名是否已经存在
        :return:
        """
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)
        if not user:
            return username
        else:
            raise ValidationError("该用户已经被注册！")

    def clean(self):
        """
        判断注册时两次密码是否一致
        :return:
        """
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致！")
