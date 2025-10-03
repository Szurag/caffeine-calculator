from django.contrib import admin

from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "caffeine_mg", "is_global", "created_by", "image_tag")
    readonly_fields = ("image_tag",)

    fieldsets = (
        (None, {
            "fields": ("name", "caffeine_mg", "is_global", "created_by", "photo", "image_tag")
        }),
    )
