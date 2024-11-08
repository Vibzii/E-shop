from django.shortcuts import render, redirect
from store.models import Product, ReviewRating
from faq.models import Question

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
    questions_unsorted = Question.objects.all()
    questions_sorted = sorted(questions_unsorted, key=lambda x: x.sort_order)

    context = {
        "questions": questions_sorted,
    }
    return render(request, "faq.html", context)


def data_policy(request):

    return render(request, "data_policy.html")


def impressum(request):
    return render(request, "impressum.html")
