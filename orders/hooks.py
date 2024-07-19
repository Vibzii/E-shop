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
from carts.models import CartItem

logger = logging.getLogger(__name__)


@csrf_exempt
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):

    ipn_obj = sender

    # Ensure the payment_status is completed
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            # Extract necessary IPN data
            transaction_id = ipn_obj.txn_id
            order_number = ipn_obj.item_number
            status = ipn_obj.payment_status
            current_user = ipn_obj.custom

            user = Account.objects.get(email=current_user)
            order = Order.objects.get(user=user.id, is_ordered=False, order_number=order_number)
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
                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variations.set(product_variation)
                    orderproduct.save()

                    # Reduce the quantity of the sold products
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()

                # Clear cart
                CartItem.objects.filter(user=user).delete()

                # Send order received email to customer
                mail_subject = 'Thank you for your order!'
                message = render_to_string('orders/order_recieved_email.html', {
                    'user': user,
                    'order': order,
                })
                to_email = user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
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