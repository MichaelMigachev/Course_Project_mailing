from django import forms
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from mailing.forms import StyleFormMixIn


User = get_user_model()  # Получаем  кастомную модель

class UserRegisterForm(StyleFormMixIn, UserCreationForm):
      class Meta:
            model = User
            fields = ('email', 'password1', 'password2')


      def clean_email(self):
            email = self.cleaned_data.get('email')

            # Проверка уникальности
            if User.objects.filter(email=email).exists():
                  raise ValidationError("Пользователь с таким email уже существует.")

            return email.lower()  # Приводим к нижнему регистру

# Модератор изменяет статус активности пользователя
class ModeratorForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

