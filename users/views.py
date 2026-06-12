from django.shortcuts import render, redirect
from django.contrib.auth import login
from Products.models import Product
from django.db.models import Sum
from Cart.models import Cart
from .forms import RegisterForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически авторизует
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('users_auth:home')  # ← исправлено: users_auth:home
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def home_page(request):
    products = Product.objects.filter(available=True)[:8]

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

    return render(request, 'users/home.html', {
        'products': products,
        'cart_count': cart_count,
        'user': request.user
    })