from django.contrib import admin
from mailing.models import Client, Message, SendAttempt, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "id",
        "email",
        "comment",
    )
    search_fields = (
        "full_name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "id",
        "letter",
    )
    search_fields = ("topic",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "first_sent_at",
        "end_at",
        "status",
    )
    list_filter = (
        "first_sent_at",
        "end_at",
        "status",
    )
    search_fields = (
        "status",
        "first_sent_at",
        "end_at",
    )


@admin.register(SendAttempt)
class SendAttempAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_time",
        "status",
        "server_response",
    )
    list_filter = (
        "attempt_time",
        "mailing",
        "status",
    )
    search_fields = ("status",)
