from django.contrib import admin

from kill.models import Product, ProductImages, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "category", "images", "price", "quantity", "description"]
    list_display = ["name", "category", "price", "quantity"]
    list_filter = ["name", "category", "price", "quantity"]


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    fields = ["image1", "image2", "image3", "image4"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
