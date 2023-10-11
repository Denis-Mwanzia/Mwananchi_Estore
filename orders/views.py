from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Orderform
import datetime
from datetime import datetime
from carts.models import CartItem
from .models import Order
# Create your views here.
def place_order(request):
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    total = 0
    quantity = 0
    grant_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax = (0.5*total)/100
    grant_total = total + tax
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_1 = form.cleaned_data['address_line_2']
            data.county = form.cleaned_data['county']
            data.city = form.cleaned_data['city']
            data.estate = form.cleaned_data['estate']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grant_total
            data.tax = tax
            data.save()
            
            #Generate Order Number
            current_date = timezone.now().strftime('%Y%m%d')
            order_number = f"{current_date}-{data.id}"  # Assuming you want to include the order ID
            data.order_number = order_number
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')