from django.contrib import admin

from .models import (
    Brand, Category, Product, ProductImage, Review, Profile,
    Wishlist, Cart, CartItem, Order, OrderItem,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'platform', 'price', 'discount_percent', 'stock', 'is_featured', 'is_active')
    list_filter = ('category', 'brand', 'platform', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'discount_percent', 'stock', 'is_featured', 'is_active')
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email')
    list_editable = ('status',)
    inlines = [OrderItemInline]


admin.site.register(Profile)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.site_header = "GameHub Administration"
admin.site.site_title = "GameHub Admin"
admin.site.index_title = "Manage Store"
