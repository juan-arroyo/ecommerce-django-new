from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category


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
        # El doble __ obtiene el valor de category_slug
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {'single_product': single_product}
        
    return render(request, 'store/product_detail.html', context)