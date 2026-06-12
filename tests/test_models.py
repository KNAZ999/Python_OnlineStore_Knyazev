from django.test import TestCase
from django.contrib.auth import get_user_model
from Products.models import Product, Category
from Cart.models import Cart, CartItem, Order


class CartModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Создайте категорию, чтобы избежать ошибки category_id
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_create_cart_for_user(self):
        """Проверка создания корзины для пользователя."""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        # OneToOneField: self.user.cart, а не self.user.cart_set
        self.assertEqual(cart, self.user.cart)

    def test_add_item_to_cart(self):
        """Проверка добавления товара в корзину."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product, quantity=2)

        self.assertEqual(cart.items.count(), 1)
        cart_item = cart.items.first()
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_item_total_price(self):
        """Проверка расчета общей стоимости товара."""
        product = Product.objects.create(
            name='Test Product',
            price=50,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product, quantity=3)

        cart_item = cart.items.first()
        self.assertEqual(cart_item.total_price, 150)

    def test_cart_total_price(self):
        """Проверка расчета общей суммы корзины."""
        product1 = Product.objects.create(
            name='Product 1',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        product2 = Product.objects.create(
            name='Product 2',
            price=50,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product1, quantity=1)
        cart.add_item(product2, quantity=2)

        self.assertEqual(cart.get_total_price(), 200)

    def test_remove_item_from_cart(self):
        """Проверка удаления товара из корзины."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product, quantity=2)
        cart.remove_item(product.id)

        self.assertEqual(cart.items.count(), 0)

    def test_clear_cart(self):
        """Проверка очистки корзины."""
        product1 = Product.objects.create(
            name='Product 1',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        product2 = Product.objects.create(
            name='Product 2',
            price=50,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product1, quantity=1)
        cart.add_item(product2, quantity=2)
        cart.clear()

        self.assertEqual(cart.items.count(), 0)

    def test_create_order(self):
        """Проверка создания заказа."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product, quantity=1)

        order = Order.objects.create(
            user=self.user,
            name='Test Customer',
            address='Test Address',
            email='test@example.com',
            cart=cart
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.name, 'Test Customer')
        self.assertEqual(order.cart, cart)

    def test_cart_str_for_user(self):
        """Проверка строкового представления корзины с пользователем."""
        cart = Cart.objects.create(user=self.user)
        expected_str = f"Корзина {self.user.username}"
        self.assertEqual(str(cart), expected_str)

    def test_cart_str_for_anonymous(self):
        """Проверка строкового представления корзины без пользователя."""
        cart = Cart.objects.create(user=None)
        expected_str = "Корзина"
        self.assertIn(expected_str, str(cart))


class ProductModelTest(TestCase):
    def setUp(self):
        # Создайте категорию, чтобы избежать ошибки category_id
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_product_creation(self):
        """Проверка создания товара."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)
        self.assertTrue(product.available)

    def test_product_str(self):
        """Проверка строкового представления товара."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        self.assertEqual(str(product), product.name)


class CartItemModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_cart_item_str(self):
        """Проверка строкового представления элемента корзины."""
        product = Product.objects.create(
            name='Test Product',
            price=100,
            category=self.category,  # ← добавлено!
            available=True
        )
        cart = Cart.objects.create(user=self.user)
        cart.add_item(product, quantity=3)

        cart_item = cart.items.first()
        self.assertEqual(str(cart_item), f"{cart_item.quantity} × {product.name}")