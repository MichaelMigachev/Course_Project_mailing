from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from mailing.forms import ClientForm, MessageForm, MailingForm , SendAttemptForm
from mailing.models import Client, Message, Mailing, SendAttempt

# mailing/views.py
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import start_mailing

# Главная страница
class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Общее количество рассылок
        context['total_mailings'] = Mailing.objects.count()

        # Количество активных рассылок (со статусом 'Запущена')
        context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()

        # Количество уникальных клиентов
        context['unique_clients'] = Client.objects.distinct().count()

        return context


# CRUD для получателей (Client)
class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    # template_name = 'client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматическое назначение владельца
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    context_object_name = 'client'
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


# CRUD для сообщений (Message)
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')

    def form_valid(self, form):
        """Автоматически назначаем текущего пользователя как владельца сообщения"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        """Ограничиваем выборку только своими рассылками"""
        return super().get_queryset().filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages_list')

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

# CRUD для рассылок (Mailing)

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Правильный способ передачи
        return kwargs


    def form_valid(self, form):
        """Автоматически назначаем владельца рассылки"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    context_object_name = 'mailings'


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем текущую рассылку
        mailing = self.get_object()
        # Добавляем получателей в контекст
        context['recipients'] = mailing.recipients.all()
        return context


# CRUD для попыток рассылки (SendAttempt)

class SendAttemptListView(LoginRequiredMixin, ListView):
    '''Список попыток'''
    model = SendAttempt  # Используем правильное имя модели
    template_name = 'mailing/send_attempt_list.html'
    context_object_name = 'send_attempts'
    paginate_by = 10  # Рекомендую добавить пагинацию

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем базовый queryset
        return queryset.filter(mailing__user=self.request.user)  # Фильтруем по пользователю

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем дополнительный контекст при необходимости
        context['title'] = 'Мои попытки рассылок'
        return context

class SendAttemptDetailView(LoginRequiredMixin, DetailView):
    model = SendAttempt
    template_name = 'mailing/send_attempt_detail.html'
    context_object_name = 'send_attempt'


class SendAttemptCreateView(LoginRequiredMixin, CreateView):
    model = SendAttempt
    template_name = 'mailing/send_attempt_form.html'
    form_class = SendAttemptForm
    success_url = reverse_lazy('send_attempt_list')


@login_required
@require_POST
def start_mailing_view(request, mailing_id):
    if not request.user == Mailing.objects.get(id=mailing_id).owner:
        return JsonResponse({"success": False, "message": "Нет прав"})
    success, message = start_mailing(mailing_id)

    if success:
        messages.success(request, "Рассылка успешно запущена!")  # Сообщение об успехе
        return redirect('mailing:mailing_list')  # Переадресация
    else:
        messages.error(request, message)  # Сообщение об ошибке
        return redirect('mailing:mailing_detail', mailing_id=mailing_id)  # Вернуться к рассылке

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
