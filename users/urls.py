from django.urls import path

from users import views
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, email_verification, UsersListView, UserUpdateView


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:token>/', views.email_verification, name='activate'),

    path('list/', UsersListView.as_view(), name='users_list'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update')
]