from django.shortcuts import render, get_object_or_404
from .models import Product, User

# Create your views here.

def home(request):
    products = Product.objects.all()

    return render(request, 'index.html', {'products': products})

def product_card(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_card.html', {'product': product})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user}) 


def cart(request):
    return render(request,'cart.html')

def news(request):
    return render(request, 'news.html')