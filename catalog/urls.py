# catalog/urls.py
"""URL-маршруты приложения catalog."""
from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home_view, name="home"),                    # /
    path("home/", views.home_view, name="home_alias"),         # /home/
    path("contacts/", views.contacts_view, name="contacts"),   # /contacts/
    path("product/create/", views.product_create_view, name="product_create"), #/новая форма/
    path("product/<int:pk>/", views.product_detail_view, name="product_detail"),  # /детальная страница товара/
    path("product/<int:pk>/edit/", views.product_update_view, name="product_update"), # добавляем update
    path("product/<int:pk>/delete/", views.product_delete_view, name="product_delete"), # добавляем delete

]
