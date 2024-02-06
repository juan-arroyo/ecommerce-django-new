from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from store.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse



# Creamos sesion para el carrito de compras (_ porque es variable local)
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@csrf_protect
@transaction.atomic
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        # Se intenta obtener el carrito de compras asociado al usuario actual
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        # Si no existe un carrito para este usuario, se crea uno nuevo
        cart = Cart.objects.create(cart_id=_cart_id(request))

    # Insertar item al carrito
    try:
        # # Se intenta encontrar un item del carrito que corresponda al producto actual y al carrito actual
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # Si el item ya existe en el carrito, se incrementa su cantidad en 1
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # Si el item no existe en el carrito, se crea uno nuevo
        cart_item = CartItem.objects.create(
            product=product,
            # Si el producto no esta en el carrito, se crea con la cantidad 1
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    # Obtenemos el carrito de compra asociado a la sesion de usuario actual
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # Obtenemos el producto especificado por su id
    product = get_object_or_404(Product, id=product_id)
    # Obtenemos el elemento del carrito que corresponde al producto y al carrito actual
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')


def remove_cart_item(request, product_id):
    # Obtenemos el carrito de compra asociado a la sesion de usuario actual
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # Obtenemos el producto especificado por su id
    product = get_object_or_404(Product, id=product_id)
    # Obtenemos el elemento del carrito que corresponde al producto y al carrito actual
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        # Obtenemos el carrito de compra asociado a la sesion de usuario actual
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Obtenemos los items del carrito de compra pasando como parametro la sesion del carrito
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total = total + (cart_item.product.price * cart_item.quantity)
            quantity = quantity + cart_item.quantity

        tax = (2*total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context = {'total': total, 'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/cart.html', context)


def actualizar_contador_carrito(request):
    # Tu lógica para contar los elementos en el carrito y devolver la cantidad
    # En este ejemplo, supondrémos que ya tienes una función llamada _cart_id(request) definida en tus vistas
    
    cart_count = 0
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if cart:
            cart_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        pass
    
    # Devuelve la cantidad de elementos en el carrito como respuesta JSON
    return JsonResponse({'cart_count': cart_count})