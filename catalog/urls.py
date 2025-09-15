"""URL-маршруты приложения catalog."""
from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home_view, name="home"),                    # /
    path("home/", views.home_view, name="home_alias"),         # /home/
    path("contacts/", views.contacts_view, name="contacts"),   # /contacts/
path("product/<int:pk>/", views.product_detail_view, name="product"),  # /детальная страница товара/
]
