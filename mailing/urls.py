from django.urls import path
from mailing.apps import MailingConfig
from . import views
# from catalog.views import ProductListView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', views.home, name='home'),


]
