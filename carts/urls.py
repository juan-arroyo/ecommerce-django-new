from django.urls import path
from .views import cart, add_cart, remove_cart, remove_cart_item,actualizar_contador_carrito


urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', remove_cart_item, name='remove_cart_item'),
    path('actualizar_contador_carrito/', actualizar_contador_carrito, name='actualizar_contador_carrito'),
]
