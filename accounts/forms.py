from django import forms
from .models import OnsideUser
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages = {
            'required':'아이디를 입력해주세요'
        },
        max_length=32, label="사용자이름")
    password = forms.CharField(
        error_messages = {
            'required':'비밀번호를 입력해주세요'
        },
        widget = forms.PasswordInput,label = "비밀번호")

    def clean(self):
        clean_data = super().clean()
        username = clean_data.get('username')
        password = clean_data.get('password')

        if username and password:
            try:
                osuser = OnsideUser.objects.get(username=username)
            except OnsideUser.DoesNotExist:
                self.add_error('username', '아이디가 없습니다.')
                return

            osuser = OnsideUser.objects.get(username=username)
            if not check_password(password, osuser.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
            else:
                self.user_id = osuser.id