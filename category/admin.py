from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    # Indicamos que el campo el lug se autocomplete en base al campo category_name
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'slug')



admin.site.register(Category, CategoryAdmin)