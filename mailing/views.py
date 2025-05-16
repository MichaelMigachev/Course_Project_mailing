from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from mailing.forms import ClientForm, MessageForm, MailingForm, SendAttemptForm, ModeratorForm
from mailing.models import Client, Message, Mailing, SendAttempt

# mailing/views.py
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import start_mailing


# Главная страница
class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_mailings"] = Mailing.objects.count()        # Общее количество рассылок

# Количество активных рассылок (со статусом 'Запущена')
        context["active_mailings"] = Mailing.objects.filter(status="Запущена").count()

# Количество уникальных клиентов
        context["unique_clients"] = Client.objects.distinct().count()

        return context


# CRUD для получателей (Client)
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"
    context_object_name = "clients"

    def get_queryset(self):

        # Проверяем, является ли текущий пользователь членом группы "Менеджеры"
        if self.request.user.groups.filter(name="Менеджер").exists():
            # Если менеджер, возвращаем полный список клиентов
            return Client.objects.all()
        else:
            # Иначе возвращаем только клиентов текущего пользователя
            return Client.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 5), name="dispatch")
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailing/client_detail.html"
    context_object_name = "client"


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    # template_name = 'client_form.html'
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматическое назначение владельца
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.owner


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    context_object_name = "client"
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.owner


# CRUD для сообщений (Message)
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        # Менеджеры видят все сообщения
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Message.objects.all()
        # Обычные пользователи — только свои
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages_list")

    def form_valid(self, form):
        """Автоматически назначаем текущего пользователя как владельца сообщения"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages_list")

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        """Ограничиваем выборку только своими рассылками"""
        return super().get_queryset().filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:messages_list")


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"


# CRUD для рассылок (Mailing)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Менеджер").exists():
            return queryset

        return queryset.filter(owner=self.request.user, is_activated=True)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Правильный способ передачи
        return kwargs

    def form_valid(self, form):
        """Автоматически назначаем владельца рассылки"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return user == mailing.owner or user.groups.filter(name="Менеджер").exists()

    def get_form_class(self):
        """Передаем владельца рассылки в форму"""
        user = self.request.user
        mailing = self.get_object()  # Получаем текущую рассылку
        # Если пользователь менеджер И НЕ владелец рассылки → ModeratorForm
        if user.groups.filter(name="Менеджер").exists() and mailing.owner != user:
            return ModeratorForm

        # Во всех остальных случаях → MailingForm
        return MailingForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Для обычных пользователей фильтруем получателей
        if not self.request.user.groups.filter(name="Менеджер").exists():
            form.fields["recipients"].queryset = Client.objects.filter(owner=self.request.user)
        return form


def get_queryset(self):
    queryset = super().get_queryset()
    # Менеджеры видят все рассылки
    if self.request.user.groups.filter(name="Менеджер").exists():
        return queryset
    # Обычные пользователи — только свои
    return queryset.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
    context_object_name = "mailings"

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем текущую рассылку
        mailing = self.get_object()
        # Добавляем получателей в контекст
        context["recipients"] = mailing.recipients.all()
        return context


# CRUD для попыток рассылки (SendAttempt)


class SendAttemptListView(LoginRequiredMixin, ListView):
    """Список попыток"""

    model = SendAttempt  # имя модели
    template_name = "mailing/send_attempt_list.html"
    context_object_name = "send_attempts"
    paginate_by = 10  # добавил пагинацию

    def get_queryset(self):

        # Сначала получаем все рассылки, принадлежащие текущему пользователю
        mailings = Mailing.objects.filter(owner=self.request.user)

        # Далее фильтруем попытки отправки, ограничивая выбор теми попытками,
        # которые относятся к найденным рассылкам
        queryset = SendAttempt.objects.filter(mailing__in=mailings)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем дополнительный контекст при необходимости
        context["title"] = "Мои попытки рассылок"
        return context


class SendAttemptDetailView(LoginRequiredMixin, DetailView):
    model = SendAttempt
    template_name = "mailing/send_attempt_detail.html"
    context_object_name = "send_attempt"


class SendAttemptCreateView(LoginRequiredMixin, CreateView):
    model = SendAttempt
    template_name = "mailing/send_attempt_form.html"
    form_class = SendAttemptForm
    success_url = reverse_lazy("send_attempt_list")


@login_required
@require_POST
def start_mailing_view(request, mailing_id):
    if not request.user == Mailing.objects.get(id=mailing_id).owner:
        return JsonResponse({"success": False, "message": "Нет прав"})
    success, message = start_mailing(mailing_id)

    if success:
        messages.success(request, "Рассылка успешно запущена!")  # Сообщение об успехе
        return redirect("mailing:mailing_list")  # Переадресация
    else:
        messages.error(request, message)  # Сообщение об ошибке
        return redirect("mailing:mailing_detail", mailing_id=mailing_id)  # Вернуться к рассылке


@login_required
def mailing_report_view(request):
    successful_send_attempts = SendAttempt.objects.filter(
        mailing__owner=request.user, status="Успешно"
    ).count()  # Получаем все попытки отправки для текущего пользователя
    unsuccessful_send_attempts = SendAttempt.objects.filter(mailing__owner=request.user, status="Не успешно").count()
    total_send_attempts = successful_send_attempts + unsuccessful_send_attempts
    context = {
        "successful_send_attempts": successful_send_attempts,
        "unsuccessful_send_attempts": unsuccessful_send_attempts,
        "total_send_attempts": total_send_attempts,
    }
    return render(request, "mailing/mailing_report.html", context)


# class SendAttemptUpdateView(LoginRequiredMixin, UpdateView):
#     model = SendAttempt
#     template_name = 'mailing/send_attempt_form.html'
#     fields = ['status', 'server_response', 'mailing']
#     success_url = reverse_lazy('send_attempt_list')  # Укажите URL
#
#
# class SendAttemptDeleteView(LoginRequiredMixin, DeleteView):
#     model = SendAttempt
#     template_name = 'mailing/send_attempt_confirm_delete.html'
#     context_object_name = 'send_attempt'
#     success_url = reverse_lazy('send_attempt_list')  # Укажите URL
