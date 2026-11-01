from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'shop/index.html')

def register(request):
    return render(request, 'shop/register.html')

def collections(request):
    category = Category.objects.filter(status=1)
    return render(request, "shop/collections.html", {"Category": category})

def collectionView(request, product):
    if Category.objects.filter(name = product, status=1):
        products = Product.objects.filter(category__name = product)
        return render(request, "shop/products/index.html", {"products": products, "category_name": product })
    else:
        messages.warning(request, "No such category found")
        print(request.build_absolute_uri())
        return redirect('collections') 

def productDetails(request, cname, pname):
    if Category.objects.filter(name=cname, status=1):
        if Product.objects.filter(name=pname, status=0):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No such product found")
            print(request.build_absolute_uri())
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        print(request.build_absolute_uri())
        return redirect('collections')

def cart(request):
    pass