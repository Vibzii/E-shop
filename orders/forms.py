from django import forms
from .models import Order
from django.utils.html import format_html
from paypal.standard.forms import PayPalPaymentsForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', "email", "address_line_1", "house_number", "address_line_2", "zipcode", "city", "country", "order_note", 'shipping_first_name', 'shipping_last_name', "shipping_address_line_1","shipping_house_number", "shipping_address_line_2", "shipping_zipcode", "shipping_city", "shipping_country"]
