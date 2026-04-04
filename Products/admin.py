from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'available')
    list_filter = ('available', 'category', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}  # если есть поле slug