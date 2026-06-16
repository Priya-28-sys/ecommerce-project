from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('home')


def checkout(request):

    cart = request.session.get('cart', {})

    order = Order.objects.create(user=request.user)

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    request.session['cart'] = {}

    return render(request, 'success.html')