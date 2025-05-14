import secrets  # Импортируем модуль для генерации случайных чисел

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings  # Импорт настроек Django
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect

from .forms import UserRegisterForm, ModeratorForm, ProfileUpdateForm


User = get_user_model()


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    # success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/activate/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, для подтверждения почты перейди по ссылке {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    User = get_user_model()
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    messages.success(request, "Email успешно подтвержден!")
    return redirect("users:login")


# Kласс для обновления профиля пользователя
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/user_form.html"
    permission_required = ["users.view_user"]

    def get_form_class(self):
        user = self.request.user
        editing_self = user == self.get_object()  # Проверяем, редактирует ли пользователь себя

        # Если пользователь имеет право set_is_active И НЕ редактирует себя
        if user.has_perm("users.set_is_active") and not editing_self:
            return ModeratorForm

        # Если модератор редактирует себя или обычный пользователь
        return ProfileUpdateForm

    def get_success_url(self):
        if self.request.user.has_perm("users.set_is_active"):
            return reverse("users:users_list")
            # Для обычного пользователя - форма профиля
        return reverse("mailing/mailing_list")
        # return reverse('users:users_list')


# Класс для просмотра списка пользователей
class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "object_list"
    ordering = "-date_joined"  # Сортировка по дате регистрации
    permission_required = ["users.view_user", "users.set_is_active"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список пользователей сервиса"
        context["users_count"] = self.get_queryset().count()
        return context
