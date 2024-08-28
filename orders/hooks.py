from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import Account
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Order, Payment, OrderProduct
from carts.models import CartItem, Cart
from decouple import config
logger = logging.getLogger(__name__)


@csrf_exempt
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    print("1")
    ipn_obj = sender
    # Ensure the payment_status is completed
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("2")
        try:
            # Extract necessary IPN data
            transaction_id = ipn_obj.txn_id
            print("3")
            order_number = ipn_obj.item_number
            status = ipn_obj.payment_status
            current_user = str(ipn_obj.custom)
            user = current_user.split("|")
            if user[0] == "True":

                user = Account.objects.get(email=user[2])
                order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
                if order:
                    # Store transaction details inside Payment model
                    payment = Payment(
                        user=user,
                        payment_id=transaction_id,
                        payment_method='Paypal',
                        amount_paid=order.order_total,
                        status=status,
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()

                    cart_items = CartItem.objects.filter(user=user)
                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.ordered = True
                        orderproduct.save()

                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variation.all()
                        # Reduce the quantity of the sold products
                        for variation in product_variation:
                            variation.stock = variation.stock - item.quantity
                            variation.save()
                            orderproduct.product_price = variation.variation_price
                            orderproduct.save()

                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variations.set(product_variation)
                        orderproduct.save()

                        # Reduce the quantity of the sold products

                    # Clear cart
                    CartItem.objects.filter(user=user).delete()

                    orderproduct = OrderProduct.objects.filter(order=order.id)

                    subtotal = 0
                    for i in orderproduct:
                        subtotal += i.product_price * i.quantity

                    # Send order received email to customer
                    mail_subject = 'Danke für deine Bestellung! 😊'
                    message = render_to_string('orders/order_received_email_user.html', {
                        'user': user.first_name,
                        'order': order,
                        'order_product': orderproduct,
                        'subtotal': subtotal,
                    })
                    to_email = user.email
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = "html"  # Ensure the email content is rendered as HTML
                    send_email.send()

                    # Send order email to Meng
                    mail_subject = 'You received an order'
                    message = render_to_string('orders/order_received_email_admin.html', {
                        'user': user,
                        'order': order,
                        'order_product': orderproduct,
                        'subtotal': subtotal,
                    })
                    to_email = "testwebshopemail@gmail.com"
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = "html"  # Ensure the email content is rendered as HTML
                    send_email.send()

                    return HttpResponse("OK")
                else:
                    logger.error(f"Order with order number {order_number} not found.")
            else:
                order = Order.objects.get(is_ordered=False, order_number=order_number)
                if order:
                    # Store transaction details inside Payment model
                    payment = Payment(
                        payment_id=transaction_id,
                        payment_method='Paypal',
                        amount_paid=order.order_total,
                        status=status,
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()

                    cart = Cart.objects.get(cart_id=user[1])
                    cart_items = CartItem.objects.filter(cart=cart)

                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.ordered = True
                        orderproduct.save()
                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variation.all()

                        # Reduce the quantity of the sold products
                        for variation in product_variation:
                            variation.stock = variation.stock - item.quantity
                            variation.save()
                            orderproduct.product_price = variation.variation_price
                            orderproduct.save()

                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variations.set(product_variation)
                        orderproduct.save()

                        # Reduce the quantity of the sold products

                    # Clear cart
                    cart = Cart.objects.get(cart_id=user[1])
                    CartItem.objects.filter(cart=cart).delete()

                    orderproduct = OrderProduct.objects.filter(order=order.id)

                    subtotal = 0
                    for i in orderproduct:
                        subtotal += i.product_price * i.quantity

                    # Send order received email to customer
                    mail_subject = 'Danke für deine Bestellung! 😊'
                    message = render_to_string('orders/order_received_email_user.html', {
                        'order': order,
                        'order_product': orderproduct,
                        'subtotal': subtotal,
                    })
                    to_email = user[2]
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = "html"  # Ensure the email content is rendered as HTML
                    send_email.send()

                    # Send order email to Meng
                    mail_subject = 'You received an order'
                    message = render_to_string('orders/order_received_email_admin.html', {
                        'user': user[2],
                        'order': order,
                        'order_product': orderproduct,
                        'subtotal': subtotal,
                    })
                    to_email = "testwebshopemail@gmail.com"
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = "html"  # Ensure the email content is rendered as HTML
                    send_email.send()

                    return HttpResponse("OK")
                else:
                    logger.error(f"Order with order number {order_number} not found.")


        except Exception as e:
            logger.error(f"Error processing IPN: {str(e)}")
    else:
        logger.warning(f"Payment not completed. Status: {ipn_obj.payment_status}")
    print("Everything done successfully")
    return HttpResponse("OK")