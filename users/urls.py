from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

from users import views
from users.apps import UsersConfig
from users.views import RegisterView, UsersListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>/", views.email_verification, name="activate"),
    path("list/", UsersListView.as_view(), name="users_list"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="update"),
    path("profile/<int:pk>", UserUpdateView.as_view(), name="profile_update"),
    #  маршруты для восстановления пароля
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/email_verification.html",
            success_url="/users/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html", success_url="/users/reset/done/"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
