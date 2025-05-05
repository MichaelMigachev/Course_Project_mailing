from django.contrib import admin
from mailing.models import User, Message, SendAttempt, Mailing


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "id", "email", "comment",)
    search_fields = ("full_name", "comment",)


@admin.register(Message)
class UserAdmin(admin.ModelAdmin):
    list_display = ("topic", "id", "letter",)
    search_fields = ("topic",)


@admin.register(Mailing)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_sent_at", "end_at", "status",)
    list_filter = ("first_sent_at", "end_at", "status",)
    search_fields = ("status", "first_sent_at", "end_at",)


@admin.register(SendAttempt)
class UserAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "server_response",)
    list_filter = ("attempt_time", "mailing", "status",)
    search_fields = ("status",)

