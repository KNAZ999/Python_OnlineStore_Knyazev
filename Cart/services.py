"""
Сервисные функции для работы с корзиной и заказами.
Эти функции изолированы от HTTP-запросов, не отображают ничего пользователю,
и предназначены для unit-тестирования.
"""

from django.db import transaction
from .models import Cart, Order


def add_to_cart_service(cart, product, quantity=1):
    """
    Добавляет товар в корзину и возвращает новую общую сумму.

    :param cart: Объект корзины (Cart)
    :param product: Объект товара (Product)
    :param quantity: Количество товара для добавления (по умолчанию 1)
    :return: Общая сумма корзины после добавления товара
    """
    cart.add_item(product, quantity)
    return cart.get_total_price()


def remove_from_cart_service(cart, product_id):
    """
    Удаляет товар из корзины по его идентификатору.

    :param cart: Объект корзины (Cart)
    :param product_id: Идентификатор товара для удаления
    """
    cart.remove_item(product_id)


def clear_cart_service(cart):
    """
    Очищает корзину полностью, удаляя все товары.

    :param cart: Объект корзины (Cart)
    """
    cart.clear()


def calculate_cart_total_service(cart):
    """
    Возвращает общую сумму корзины без изменения её содержимого.

    :param cart: Объект корзины (Cart)
    :return: Общая сумма корзины (float)
    """
    return cart.get_total_price()


def place_order_service(cart, name, address, email, user=None):
    """
    Оформляет заказ на основе корзины.
    Выполняет очистку корзины и сохранение заказа в базе данных.

    :param cart: Объект корзины (Cart)
    :param name: Имя клиента (str)
    :param address: Адрес доставки (str)
    :param email: Email клиента (str)
    :param user: Пользователь (User, optional)
    :return: Объект заказа (Order)
    :raises ValueError: Если корзина пуста
    """
    if not cart.items.exists():
        raise ValueError("Корзина пуста")

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            name=name,
            address=address,
            email=email,
            cart=cart
        )
        cart.clear()
        return order


def get_orders_by_status_service(user=None, session_id=None, status='completed'):
    """
    Возвращает список заказов по статусу и/или пользователю.

    :param user: Пользователь (User, optional)
    :param session_id: ID сессии (str, optional)
    :param status: Статус заказа (str, по умолчанию 'completed')
    :return: QuerySet объектов Order
    """
    if user:
        orders = Order.objects.filter(user=user, status=status)
    elif session_id:
        orders = Order.objects.filter(cart__session_id=session_id, status=status)
    else:
        orders = Order.objects.filter(status=status)
    return orders