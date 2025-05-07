import secrets # Импортируем модуль для генерации случайных чисел

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import login, get_user_model
from django.core.mail import send_mail
from django.conf import settings  # Импорт настроек Django
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect

from .forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    # success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/activate/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, для подтверждения почты перейди по ссылке {url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list = [user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    User = get_user_model()
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    messages.success(request, "Email успешно подтвержден!")
    return redirect('users:login')

