from django.db import models
from django.conf import settings
from Products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def add_item(self, product, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': 0}
        )
        item.quantity += quantity
        item.save()

    def __str__(self):
        return f"Корзина {self.user.username}" if self.user else "Анонимная корзина"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    email = models.EmailField(verbose_name="Email")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ от {self.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"