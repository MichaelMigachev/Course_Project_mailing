from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (
    HomeView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDetailView,
    ClientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MessageDetailView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingDetailView,
    SendAttemptListView,
    SendAttemptDetailView,
    SendAttemptCreateView,
)
from .views import start_mailing_view, mailing_report_view


app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # Client URLS
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    # Message URLS
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("messages/create/", MessageCreateView.as_view(), name="messages_create"),
    path("messages/update/<int:pk>/", MessageUpdateView.as_view(), name="messages_update"),
    path("messages/delete/<int:pk>/", MessageDeleteView.as_view(), name="messages_delete"),
    path("messages/detail/<int:pk>/", MessageDetailView.as_view(), name="messages_detail"),
    # Mailing URLS
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/detail/<int:pk>/", cache_page(60)(MailingDetailView.as_view()), name="mailing_detail"),
    # SendAttempt URLS
    path("send_attempt/", SendAttemptListView.as_view(), name="send_attempt_list"),
    path("send_attempt/<int:pk>/", SendAttemptDetailView.as_view(), name="send_attempt_detail"),
    path("send_attempt/create/", SendAttemptCreateView.as_view(), name="send_attempt_create"),
    # path('send_attempt/<int:pk>/update/', SendAttemptUpdateView.as_view(), name='send_attempt_update'),
    # path('send_attempt/<int:pk>/delete/', SendAttemptDeleteView.as_view(), name='send_attempt_delete'),
    #  URLS для кнопки запуска рассылки
    path("start/<int:mailing_id>/", start_mailing_view, name="start_mailing"),
    #  URLS для страници с отчетами
    path("report/", mailing_report_view, name="report"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
