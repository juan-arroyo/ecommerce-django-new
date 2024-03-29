from django.db import models
from category.models import Category
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    # Creación de URL/LINK dínamico
    def get_url(self):
        # La funcion revervse hace referencia a la vista llamada product_detail y lleva dos argumentos ya que la url de dicha vista se pasan dos argumentos : path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail')
        return reverse('product_detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name
