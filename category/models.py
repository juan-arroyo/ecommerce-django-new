from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    # Creación de URL/LINK dínamico
    def get_url(self):
        # La funcion revervse hace referencia a la vista llamada product_by_category y lleva dos argumentos ya que la url de dicha vista se pasa 1 argumento : path('<slug:category_slug>/', store, name='product_by_category'),
        return reverse('product_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
