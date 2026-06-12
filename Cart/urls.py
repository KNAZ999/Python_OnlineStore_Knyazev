from django.urls import path
from . import views

app_name = 'Cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),  # ← новый маршрут
]