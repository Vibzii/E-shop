from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, Category, ReviewRating, ProductGallery, Variation
from orders.models import OrderProduct
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    sort_by = request.GET.get('sort')  # Get the sorting option from the request, default to None
    order = request.GET.get('order', 'asc')  # Get the order (ascending or descending), default to 'asc'

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        if sort_by == 'price':
            if order == 'desc':
                products = Product.objects.filter(category=categories, is_available=True).order_by("-price")
            else:
                products = Product.objects.filter(category=categories, is_available=True).order_by("price")
        else:
            products = Product.objects.filter(category=categories, is_available=True).order_by("-created_date")
        paginator = Paginator(products, 100)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        if sort_by == 'price':
            if order == 'desc':
                products = Product.objects.filter(is_available=True).order_by("-price")
            else:
                products = Product.objects.filter(is_available=True).order_by("price")
        else:
            products = Product.objects.filter(is_available=True).order_by("-created_date")
        paginator = Paginator(products, 100)
        page= request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        "products": paged_products,
        "product_count": product_count,
        'current_sort': sort_by,
        'current_order': order,

    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    else:
        order_product = False

    category = Category.objects.get(slug=category_slug)

    #Get the reviews :

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    variations = Variation.objects.filter(product=single_product)
    if request.user.is_authenticated:
        user_reviewed = ReviewRating.objects.filter(product=single_product, user=request.user).exists()
    else:
        user_reviewed = False



    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    gallery_sorted = sorted(product_gallery, key=lambda x: x.sort_order)
    count_gallery = product_gallery.count()

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': gallery_sorted,
        'variations': variations,
        'count_gallery': count_gallery,
        'category_slug': category_slug,
        'product_slug': product_slug,
        'category': category,
        'user_reviewed': user_reviewed,
    }

    return render(request,'store/product-detail.html', context)

def search(request):
    products = None
    product_count = None
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()


    context ={
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")

                return redirect(url)
            else:
                messages.error(request, "There was an error submitting your review. Please try again.")


