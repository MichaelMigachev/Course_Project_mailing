from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


from mailing.forms import ClientForm, MessageForm, MailingForm , SendAttemptForm
from mailing.models import Client, Message, Mailing, SendAttempt


# Create your views here.
# def home(request):
#     return render(request, 'mailing/home.html')

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


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    # template_name = 'client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    context_object_name = 'client'
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


# CRUD для сообщений (Message)
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages_list')

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

# CRUD для рассылок (Mailing)

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
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

class SendAttemptListView(ListView):
    '''Список попыток'''
    model = SendAttempt
    template_name = 'mailing/send_attempt_list.html'
    context_object_name = 'send_attempts'


class SendAttemptDetailView(DetailView):
    model = SendAttempt
    template_name = 'mailing/send_attempt_detail.html'
    context_object_name = 'send_attempt'


class SendAttemptCreateView(CreateView):
    model = SendAttempt
    template_name = 'mailing/send_attempt_form.html'
    form_class = SendAttemptForm
    success_url = reverse_lazy('send_attempt_list')


# class SendAttemptUpdateView(UpdateView):
#     model = SendAttempt
#     template_name = 'mailing/send_attempt_form.html'
#     fields = ['status', 'server_response', 'mailing']
#     success_url = reverse_lazy('send_attempt_list')  # Укажите URL
#
#
# class SendAttemptDeleteView(DeleteView):
#     model = SendAttempt
#     template_name = 'mailing/send_attempt_confirm_delete.html'
#     context_object_name = 'send_attempt'
#     success_url = reverse_lazy('send_attempt_list')  # Укажите URL
