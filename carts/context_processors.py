from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0

    try:
        # Intentamos encontrar el carrito de compras asociado con la sesión actual
        cart = Cart.objects.filter(cart_id=_cart_id(request))

        # Obtenemos todos los elementos del carrito que pertenecen al carrito encontrado (limitado a 1, o sea el primer carrito de compra, ya que puede tener varios)
        # Dado que el ID del carrito debe ser único, solo se espera un carrito en la lista
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
        print(cart_items)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    
    except Cart.DoesNotExist:
        cart_count = 0
    
    context = {'cart_count':cart_count}
    return context

