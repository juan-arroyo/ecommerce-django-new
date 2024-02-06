from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id


def store(request, category_slug=None):

    if category_slug != None:
        # Obtenemos la categoría específica si se proporciona un slug de categoría
        categories = get_object_or_404(Category, slug=category_slug)
         # Filtramos los productos basados en la categoría seleccionada y si están disponibles
        products = Product.objects.filter(category = categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        # Contamos los productos a partir de la instancia de products
        product_count = products.count()
    
    context = {'products_store': products,
               'product_count_store': product_count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # # Intenta obtener un producto que coincida con el slug de la categoría y el slug del producto. El doble __ obtiene el valor de category_slug
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # Verifica si el producto está en el carrito de compras
        # Primero, obtenemos el carrito actual del usuario utilizando la función _cart_id(request)
        # Luego, verificamos si hay un objeto CartItem que coincida con el carrito actual y el producto
        # exists() devuelve True si hay algún objeto CartItem que cumpla con los criterios de filtro
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    
    context = {'single_product': single_product, 'in_cart':in_cart}
        
    return render(request, 'store/product_detail.html', context)