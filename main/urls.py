from django.urls import path
from .views import *

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('products', products, name='products'),
    path('products/category/<int:category_id>/', products, name='products_by_category'),
    path('productdetail/<int:product_id>', productdetail, name='productdetail'),
    path('longread', longread, name='longread'),
    path('support', support, name='support'),
    path('registration', registration, name='registration'),
    path('authorization', authorization, name='authorization'),
    path('cart', cart, name='cart'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>', remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:product_id>', update_cart_quantity, name='update_cart_quantity'),
    path('create_order/', create_order, name='create_order'),
    path('profil', profil, name='profil'),
    path('my-orders/', my_orders, name='my_orders'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('toggle-favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', favorites_list, name='favorites_list'),
    path('logout', logout_view, name='logout'),
]