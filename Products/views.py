from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Sum
from Cart.models import Cart  # ← ДОБАВЛЕНО! Это исправит ошибку


def product_list(request):
    products = Product.objects.all()

    # Подсчёт количества товаров в корзине
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    else:
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.filter(session_id=session_id).first()
            if cart:
                cart_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, 'Products/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})