from django.shortcuts import render, redirect
from store.models import Product, ReviewRating

def home(request):

    products = Product.objects.filter(is_available=True).order_by("-created_date")[:4]

    #Get the reviews :
    reviews = None
    try:
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    finally:

        context = {
            "products": products,
            "reviews": reviews,
        }

        return render(request, "home.html", context)


def faq(request):

    return render(request, "faq.html")
