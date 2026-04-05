from django.urls import path
from .views import add_to_cart, place_order

urlpatterns = [
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('place_order/', place_order, name='place_order'),
]