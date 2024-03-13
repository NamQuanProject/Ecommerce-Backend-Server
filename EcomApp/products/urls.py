from django.urls import path

from . import views

urlpatterns = [
    path("", views.product),
    path("own_product", views.own_product),
    path("shopping", views.shopping),
    path("cart", views.shoppingCart),
    path("make_order", views.make_order_from_cart),
    path("order", views.order),
]



