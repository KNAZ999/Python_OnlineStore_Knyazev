from django.db import models
from django.db.models import Sum
from django.conf import settings


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    session_id = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="ID сессии"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"Корзина {self.user.username}" if self.user else "Корзина"

    def add_item(self, product, quantity=1):
        """
        Добавляет товар в корзину или увеличивает его количество, если он уже есть.

        :param product: Объект товара (Product)
        :param quantity: Количество товара для добавления (по умолчанию 1)
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_item(self, product_id):
        """
        Удаляет товар из корзины по ID.

        :param product_id: Идентификатор товара
        """
        CartItem.objects.filter(cart=self, product_id=product_id).delete()

    def clear(self):
        """
        Очищает корзину полностью, удаляя все элементы.
        """
        CartItem.objects.filter(cart=self).delete()

    def get_total_price(self):
        """
        Возвращает общую сумму всех товаров в корзине, учитывая количество.

        :return: Общая сумма (Decimal)
        """
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        "Products.Product",
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    name = models.CharField(max_length=100, verbose_name="Имя")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    email = models.EmailField(verbose_name="Email")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"Заказ #{self.id} от {self.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"