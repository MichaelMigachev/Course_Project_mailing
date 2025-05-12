from django import forms
from django.forms import BooleanField
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Client, Message, Mailing, SendAttempt


class StyleFormMixIn:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ClientForm(StyleFormMixIn, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise ValidationError("Пожалуйста, введите ваше полное имя.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Пожалуйста, введите email.")
        # проверка на корректность email, например:
        from django.core.validators import validate_email
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Некорректный email адрес.")
        return email

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        # ограничение по длине комментария
        if comment and len(comment) > 150:
            raise ValidationError("Комментарий не должен превышать 150 символов.")
        return comment


class MessageForm(StyleFormMixIn, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'letter']

    def clean_topic(self):
        topic = self.cleaned_data.get('topic')
        if not topic:
            raise ValidationError("Пожалуйста, введите тему сообщения.")
        if len(topic) > 100:
            raise ValidationError("Тема не должна превышать 100 символов.")
        return topic

    def clean_letter(self):
        letter = self.cleaned_data.get('letter')
        if not letter:
            raise ValidationError("Пожалуйста, введите текст письма.")
        if len(letter) < 10:
            raise ValidationError("Текст письма должен содержать как минимум 10 символов.")
        return letter


class MailingForm(StyleFormMixIn, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['first_sent_at', 'end_at', 'status', 'message', 'recipients']

    def clean(self):
        cleaned_data = super().clean()
        first_sent_at = cleaned_data.get('first_sent_at')
        end_at = cleaned_data.get('end_at')
        status = cleaned_data.get('status')

        # Проверка, что даты заданы и правильный порядок
        if first_sent_at and end_at:
            if first_sent_at >= end_at:
                raise ValidationError("Дата начала рассылки должна быть раньше даты окончания.")
            # Проверка, что даты не в прошлом
            if first_sent_at < timezone.now():
                self.add_error('first_sent_at', "Дата начала не может быть в прошлом.")

        # Проверка статуса (например, что выбран допустимый статус)
        valid_statuses = ['Создана', 'Запущена', 'Завершена']
        if status not in valid_statuses:
            self.add_error('status', 'Недопустимый статус рассылки.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        # Достаем пользователя перед вызовом родительского __init__
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фильтруем получателей только для текущего пользователя
        if self.user:
            self.fields['recipients'].queryset = Client.objects.filter(owner=self.user)
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)


class SendAttemptForm(StyleFormMixIn, forms.ModelForm):
    class Meta:
        model = SendAttempt
        fields = ['status', 'server_response', 'mailing']
