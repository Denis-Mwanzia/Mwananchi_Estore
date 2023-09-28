from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # get the product for our cart
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Exception as e:
                pass

    try:
        # get the cart id from the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(cart=cart, product=product).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        #logic to handling variation
        #existing variations - db
        #current variations - product variations
        #item id - db
        ex_var_list = []
        id_item = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id_item.append(item.id)
        print(ex_var_list)
        
        if product_variation in ex_var_list:
            #increase cart_item objects
            index = ex_var_list.index(product_variation)
            item_id = id_item[index]
            item = CartItem.objects.get(id=item_id, product=product)
            item.quantity += 1
            item.save()     
        else:
            #create a new cart item
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product_id = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product_id, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product_id = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product_id, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grant_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0.5*total)/100
        grant_total = total + tax
    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grant_total': grant_total,
    }

    return render(request, 'store/cart.html', context)
