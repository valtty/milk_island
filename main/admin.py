from django.contrib import admin
from .models import Profile, Category, Product, Cart, CartItem, Order, OrderItem, Review, Favorite

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    fields = ('name', 'icon')

admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Favorite)
