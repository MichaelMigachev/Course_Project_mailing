from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
# from users.views import RegisterView


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='mailing:products_list'), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
]