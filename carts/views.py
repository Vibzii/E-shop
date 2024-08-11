from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id, item_quantity=1):

    current_user = request.user
    product = Product.objects.get(id=product_id)
    #redirection is set in HTML Product Detail
    redirect_url = request.GET.get('next', 'cart')
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            try:
                item_quantity = int(request.POST.get('quantity'))
            except:
                pass
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_items_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variation.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += item_quantity
                stock_quantity = 0
                for i in item.variation.all():
                    if i.stock > stock_quantity:
                        stock_quantity = i.stock
                if stock_quantity < item.quantity:
                    item.quantity = stock_quantity
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=item_quantity, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)

                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=item_quantity,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)

            cart_item.save()

        return redirect(redirect_url)


    #If Not Authenticated
    else:

        product_variation = []

        if request.method == "POST":
            try:
                item_quantity = int(request.POST.get('quantity'))
            except:
                pass
            for item in request.POST:
                key= item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_items_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variation.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=item_quantity
                stock_quantity = 0
                for i in item.variation.all():
                    if i.stock > stock_quantity:
                        stock_quantity = i.stock
                if stock_quantity < item.quantity:
                    item.quantity = stock_quantity
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=item_quantity, cart=cart)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)

                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity=item_quantity,
                cart=cart,
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)

            cart_item.save()
        return redirect(redirect_url)

def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else :
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')
def update_cart_quantity(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None, max_shipping=0, grand_total=0):


    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        max_shipping = 0
        for cart_item in cart_items:
            for item in cart_item.variation.all():
                total += (item.variation_price * cart_item.quantity)
                quantity += cart_item.quantity

            if cart_item.product.shipping > max_shipping:
                max_shipping= cart_item.product.shipping

        #tax = (0 * total)/100
        grand_total = total + max_shipping
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_cost': max_shipping,
        #'tax': tax,
        #'grand_total': grand_total
    }


    return render(request, 'store/cart.html', context)
def checkout(request, total=0, quantity=0,grand_total=0, cart_items=None, max_shipping=0):
    try:
        tax=0
        grand_total =0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        max_shipping = 0
        for cart_item in cart_items:
            for item in cart_item.variation.all():
                total += (item.variation_price * cart_item.quantity)
                quantity += cart_item.quantity

            if cart_item.product.shipping > max_shipping:
                max_shipping = cart_item.product.shipping


        #tax = (0 * total) / 100
        grand_total = total + max_shipping


    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'grand_total': grand_total,
        'shipping': max_shipping,
        'quantity': quantity,
        'cart_items': cart_items,
        #'tax': tax,
    }
    return render(request, "store/checkout.html", context)