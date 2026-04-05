from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Products.models import Product
from .forms import CartForm
from .models import Cart

def place_order(request):
    # Пока заглушка
    return render(request, 'Cart/place_order.html')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product'].id  # Получаем ID товара
            quantity = form.cleaned_data['quantity']

            # Получаем или создаём корзину пользователя
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Находим товар
            product = get_object_or_404(Product, id=product_id)

            # Добавляем товар в корзину
            cart.add_item(product, quantity)

            return redirect('Products:product_list')  # Перенаправляем в каталог
    else:
        # При GET-запросе форма создаётся без данных
        form = CartForm()

    return render(request, 'Cart/add_to_cart.html', {'form': form})