from django.urls import path, include
from . import views

urlpatterns = [

    path('payment_product/', views.payment_product, name='payment-product'),
    path('payment-success/<int:order_number>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    path('paypal/', include("paypal.standard.ipn.urls")),

]