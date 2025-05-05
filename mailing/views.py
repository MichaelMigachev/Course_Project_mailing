from django.shortcuts import render
from django.urls import reverse_lazy
from mailing.models import User, Message, Mailing, SendAttempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


# Create your views here.
# def home(request):
#     return render(request, 'mailing/home.html')

# Главная страница

class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total_mailings'] = NewsLetter.objects.count()
    #     context['active_mailings'] = NewsLetter.objects.filter(status='Запущена').count()
    #     context['unique_recipients'] = User.objects.count()
    #     return context


# CRUD для получателей (User)
class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'mailing/user_detail.html'
    context_object_name = 'user'


class UserCreateView(CreateView):
    model = User
    fields = ('full_name', 'email', 'comment')
    # template_name = 'user_form.html'
    success_url = reverse_lazy('mailing:user_list')


class UserUpdateView(UpdateView):
    model = User
    fields = ('full_name', 'email', 'comment')
    template_name = 'mailing/user_form.html'
    success_url = reverse_lazy('mailing:user_list')


class UserDeleteView(DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'mailing/user_confirm_delete.html'
    success_url = reverse_lazy('mailing:user_list')


# CRUD для сообщений (Message)
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    fields = ('topic', 'letter')
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('topic', 'letter')
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
    fields = ('status', 'message', 'recipients', 'first_sent_at', 'end_at')
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('status', 'message', 'recipients', 'first_sent_at', 'end_at')
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
    fields = ['status', 'server_response']
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
