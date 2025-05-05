from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (HomeView, UserListView, UserCreateView, UserUpdateView, UserDetailView, UserDeleteView,
                           MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView,
                           MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView,
                           SendAttemptListView, SendAttemptDetailView, SendAttemptCreateView,
                           )

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name="home"),

    # User URLS
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    # Message URLS
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/create/', MessageCreateView.as_view(), name='messages_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='messages_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='messages_delete'),
    path('messages/detail/<int:pk>/', MessageDetailView.as_view(), name='messages_detail'),
    # Mailing URLS
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    # SendAttempt URLS
    path('send_attempt/', SendAttemptListView.as_view(), name='send_attempt_list'),
    path('send_attempt/<int:pk>/', SendAttemptDetailView.as_view(), name='send_attempt_detail'),
    path('send_attempt/create/', SendAttemptCreateView.as_view(), name='send_attempt_create'),
    # path('send_attempt/<int:pk>/update/', SendAttemptUpdateView.as_view(), name='send_attempt_update'),
    # path('send_attempt/<int:pk>/delete/', SendAttemptDeleteView.as_view(), name='send_attempt_delete'),
]
