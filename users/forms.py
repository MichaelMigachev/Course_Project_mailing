from django import forms
from django.contrib.auth.forms import UserCreationForm
# from mailing.forms import StyleFormMixin
class UserRegisterForm(UserCreationForm):
      class Meta:
            model = User
            fields = ('email', 'password1', 'password2')


