"""URL-маршруты приложения catalog (CBV)."""
from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView, ProductCreateView

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),                                 # /
    path("home/", HomeView.as_view(), name="home_alias"),                      # /home/
    path("contacts/", ContactsView.as_view(), name="contacts"),                # /contacts/
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product"),    # /product/<pk>/
    path("product/create/", ProductCreateView.as_view(), name="product_create")# /product/create/
]