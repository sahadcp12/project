from django.shortcuts import render, redirect, get_object_or_404

from shop_app.models import product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart_app=request.session.session_key
    if not cart_app:
        cart_app=request.session.create()
    return cart_app
def add_cart(request,product_id):
    Product=product.objects.get(id=product_id)
    try:
        cart_app = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_app = Cart.objects.create(cart_id=_cart_id(request))
        cart_app.save(),
    try:
        cart_item = CartItem.objects.get(Product=Product,cart_app=cart_app)
        if cart_item.quantity < cart_item.Product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            Product=Product,
            quantity=1,
            cart_app=cart_app
        )
        cart_item.save()
    return redirect('cart_app:cart_detail')
def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart_app=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart_app=cart_app,active=True)
        for cart_item in cart_items:
            total += (cart_item.Product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))



def cart_remove(request,product_id):
    cart_app=Cart.objects.get(cart_id=_cart_id(request))
    Product=get_object_or_404(product,id=product_id)
    cart_item=CartItem.objects.get(Product=Product,cart_app=cart_app)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_detail')
def full_remove(request,product_id):
    cart_app = Cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    cart_item = CartItem.objects.get(Product=Product, cart_app=cart_app)
    cart_item.delete()
    return redirect('cart_app:cart_detail')