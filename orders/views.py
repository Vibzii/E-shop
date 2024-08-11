# *====================  ALL IMPORTS ======================== #
from django.shortcuts import render, redirect
from carts.models import CartItem, Cart
from carts.views import _cart_id
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct





# *====================  STEP 1 FUNCTION  ======================== #

def payment_product(request):

    if request.user.is_authenticated:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        print(current_user)
    else:
        try:
        # Fetch the session cart
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            return redirect("login")


    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    max_shipping = 0
    for cart_item in cart_items:
        for item in cart_item.variation.all():
            total += (item.variation_price * cart_item.quantity)
            quantity += cart_item.quantity

        if cart_item.product.shipping > max_shipping:
            max_shipping = cart_item.product.shipping

    tax = (0 * total) / 100
    grand_total = total + tax + max_shipping
    host = request.get_host()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            if request.user.is_authenticated:
                data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            #data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.zipcode = form.cleaned_data['zipcode']
            data.city = form.cleaned_data['city']
            data.shipping_name = form.cleaned_data['shipping_name']
            data.shipping_address_line_1 = form.cleaned_data['shipping_address_line_1']
            data.shipping_address_line_2 = form.cleaned_data['shipping_address_line_2']
            data.shipping_country = form.cleaned_data['shipping_country']
            data.shipping_zipcode = form.cleaned_data['shipping_zipcode']
            data.shipping_city = form.cleaned_data['shipping_city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.shipping_cost = max_shipping
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(id=data.id, is_ordered=False, order_number=order_number)
            # Generate item names from cart items
            item_names = [item.product.product_name for item in cart_items]
            item_name_str = ', '.join(item_names)

            paypal_checkout = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'custom': current_user if request.user.is_authenticated else 'data.email',
                'amount': grand_total,
                'item_name': item_name_str,
                'invoice': str(uuid.uuid4()),  # Ensure this is a string
                'currency_code': 'EUR',
                "item_number": order_number,
                'notify_url': f"https://{host}{reverse('paypal-ipn')}",
                'return_url': f"http://{host}{reverse('payment-success', kwargs={'order_number': order_number})}",
                'cancel_url': f"http://{host}{reverse('payment-failed')}",
            }

            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'shipping': max_shipping,
                'paypal': paypal_payment,
            }

            return render(request, 'orders/payments.html', context)

    else:

        return redirect("checkout")

    # *====================  STEP 2 FUNCTION  ======================== #


def PaymentSuccessful(request, order_number):

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = order.payment  # Directly access the payment field of the order

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id if payment else None,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')

    # *====================  STEP 3 FUNCTION  ======================== #


def paymentFailed(request):
    product = "All Items"

    return render(request, 'store/payment-failed.html', {'product': product})

    # *====================  STEP 4 FUNCTION  ======================== #


