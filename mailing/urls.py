from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import HomeView
# from catalog.views import ProductListView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name="home"),


]
