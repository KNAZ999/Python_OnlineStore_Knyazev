from django import forms
from Products.models import Product
from Cart.models import Cart


class CartForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.HiddenInput()  # Прячем поле, так как товар выбирается автоматически
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Количество",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class OrderForm(forms.Form):
    name = forms.CharField(label="Ваше имя", required=True)
    address = forms.CharField(label="Адрес доставки", required=True)
    email = forms.EmailField(label="Электронная почта", required=True)
    cart = forms.ModelChoiceField(queryset=Cart.objects.none(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)
        if cart:
            self.fields['cart'].queryset = Cart.objects.filter(pk=cart.pk)
            self.fields['cart'].initial = cart