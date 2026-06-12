"""
Модуль unit-тестов для сервисных функций корзины и оформления заказа.
Тесты проверяют изолированную бизнес-логику без HTTP-зависимостей.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from Products.models import Product, Category
from Cart.models import Cart, CartItem, Order
from Cart.services import (
    add_to_cart_service,
    remove_from_cart_service,
    clear_cart_service,
    calculate_cart_total_service,
    place_order_service,
)


class CartServiceTest(TestCase):
    """
    Набор тестов для проверки сервисных функций работы с корзиной и заказами.
    Все тесты используют изолированные функции, не зависящие от HTTP-запросов.
    """

    def setUp(self):
        """
        Инициализация тестовых данных перед каждым тестом.
        Создаётся пользователь, категория и два тестовых товара.
        """
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product1 = Product.objects.create(
            name="Product 1", price=100, category=self.category, available=True
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=50, category=self.category, available=True
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart_service(self):
        """
        Проверка добавления товара в корзину через сервис-функцию.

        Убеждается, что начальная цена корзины равна 0,
        добавляет товар и проверяет правильность подсчёта суммы,
        а также количество товара в корзине.
        """
        # Проверка начального состояния корзины
        initial_price = calculate_cart_total_service(self.cart)
        self.assertEqual(initial_price, 0, "Начальная сумма корзины должна быть 0")

        # Добавление товара и проверка итоговой суммы
        final_price = add_to_cart_service(self.cart, self.product1, quantity=2)
        self.assertEqual(
            final_price, 200, "Сумма корзины после добавления должна быть 200"
        )

        # Проверка создания элемента корзины
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product1)
        self.assertEqual(cart_item.quantity, 2, "Количество товара должно быть 2")

    def test_remove_from_cart_service(self):
        """
        Проверка удаления товара из корзины через сервис-функцию.

        Добавляет товар, удаляет его и проверяет, что корзина пуста.
        """
        # Добавление товара перед удалением
        self.cart.add_item(self.product1, quantity=2)
        self.assertEqual(self.cart.items.count(), 1, "Корзина должна содержать 1 товар")

        # Удаление товара
        remove_from_cart_service(self.cart, self.product1.id)
        self.assertEqual(
            self.cart.items.count(), 0, "Корзина должна быть пуста после удаления"
        )

    def test_clear_cart_service(self):
        """
        Проверка полной очистки корзины через сервис-функцию.

        Добавляет несколько товаров и проверяет, что корзина полностью очищается.
        """
        # Добавление нескольких товаров
        self.cart.add_item(self.product1, quantity=1)
        self.cart.add_item(self.product2, quantity=2)
        self.assertEqual(
            self.cart.items.count(), 2, "Корзина должна содержать 2 товара"
        )

        # Очистка корзины
        clear_cart_service(self.cart)
        self.assertEqual(
            self.cart.items.count(), 0, "Корзина должна быть пуста после очистки"
        )

    def test_calculate_cart_total_service(self):
        """
        Проверка корректности подсчёта общей суммы корзины.

        Добавляет товары с разным количеством и проверяет итоговую сумму.
        """
        # Добавление товаров
        self.cart.add_item(self.product1, quantity=2)
        self.cart.add_item(self.product2, quantity=3)

        # Проверка итоговой суммы
        total = calculate_cart_total_service(self.cart)
        expected_total = 2 * 100 + 3 * 50  # 200 + 150 = 350
        self.assertEqual(
            total,
            expected_total,
            f"Ожидаемая сумма: {expected_total}, получено: {total}",
        )

    def test_place_order_service(self):
        """
        Проверка успешного оформления заказа через сервис-функцию.

        Добавляет товары, оформляет заказ и проверяет:
        - Данные заказа соответствуют введённым,
        - Связь с корзиной установлена верно,
        - Корзина автоматически очищается после оформления.
        """
        # Добавление товаров в корзину
        self.cart.add_item(self.product1, quantity=1)
        self.cart.add_item(self.product2, quantity=2)

        # Оформление заказа
        order = place_order_service(
            cart=self.cart,
            name="Test Customer",
            address="Test Address",
            email="test@example.com",
            user=self.user,
        )

        # Проверка данных заказа
        self.assertEqual(order.user, self.user, "Пользователь заказа должен совпадать")
        self.assertEqual(order.name, "Test Customer", "Имя клиента должно совпадать")
        self.assertEqual(
            order.cart, self.cart, "Связь с корзиной должна быть установлена"
        )

        # Проверка очистки корзины
        self.assertEqual(
            self.cart.items.count(),
            0,
            "Корзина должна быть очищена после оформления заказа",
        )

    def test_place_order_service_empty_cart(self):
        """
        Проверка обработки ошибки при попытке оформить заказ с пустой корзиной.

        Ожидается, что сервисная функция вызовет ValueError с сообщением 'Корзина пуста'.
        """
        # Попытка оформить заказ с пустой корзиной
        with self.assertRaises(ValueError) as context:
            place_order_service(
                cart=self.cart,
                name="Test Customer",
                address="Test Address",
                email="test@example.com",
                user=self.user,
            )

        # Проверка сообщения об ошибке
        self.assertEqual(
            str(context.exception),
            "Корзина пуста",
            "Сообщение об ошибке должно быть 'Корзина пуста'",
        )