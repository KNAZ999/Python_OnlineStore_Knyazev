"""
Представления для работы с корзиной и заказами.
Все view-функции используют сервисные функции из Cart/services.py.
"""

from django.shortcuts import render, redirect, get_object_or_404
from Products.models import Product
from .models import Cart, Order
from django.contrib import messages
from django.db.models import Sum
from .services import place_order_service


def _get_cart(request):
    """
    Получает корзину для пользователя или анонимного клиента.

    :param request: HTTP-запрос
    :return: Объект корзины (Cart)
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_id=session_id,
            defaults={'user': None}
        )
        return cart


def add_to_cart(request, product_id):
    """
    Добавляет товар в корзину и перенаправляет на страницу каталога.

    :param request: HTTP-запрос
    :param product_id: Идентификатор товара
    """
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart.add_item(product, quantity=1)
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('Products:product_list')


def remove_from_cart(request, product_id):
    """
    Удаляет товар из корзины и перенаправляет на страницу корзины.

    :param request: HTTP-запрос
    :param product_id: Идентификатор товара
    """
    cart = _get_cart(request)
    cart.remove_item(product_id)
    messages.info(request, 'Товар удалён из корзины')
    return redirect('Cart:cart_detail')


def clear_cart(request):
    """
    Очищает корзину и перенаправляет на страницу корзины.

    :param request: HTTP-запрос
    """
    cart = _get_cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена')
    return redirect('Cart:cart_detail')


def cart_detail(request):
    """
    Отображает страницу корзины пользователя.

    :param request: HTTP-запрос
    :return: HTTP-ответ с шаблоном корзины
    """
    cart = _get_cart(request)
    return render(request, 'Cart/cart_detail.html', {'cart': cart})


def place_order(request):
    """
    Оформляет заказ на основе корзины.
    Использует place_order_service для проверки и сохранения заказа.

    :param request: HTTP-запрос
    :return: HTTP-ответ с формой или перенаправлением
    """
    cart = _get_cart(request)

    if not cart.items.exists():
        messages.error(request, 'Корзина пуста')
        return redirect('Cart:cart_detail')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        if not all([name, address, email]):
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'Cart/place_order.html', {'cart': cart})

        try:
            order = place_order_service(
                cart=cart,
                name=name,
                address=address,
                email=email,
                user=cart.user if cart.user else None
            )
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('Cart:order_list')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'Cart/place_order.html', {'cart': cart})

    return render(request, 'Cart/place_order.html', {'cart': cart})


def order_list(request):
    """
    Отображает список заказов пользователя.

    :param request: HTTP-запрос
    :return: HTTP-ответ со списком заказов
    """
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = Order.objects.filter(cart__session_id=request.session.session_key).order_by('-created_at')

    return render(request, 'Cart/order_list.html', {'orders': orders})