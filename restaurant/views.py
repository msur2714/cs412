from django.shortcuts import render
import random
from time import time


# Create your views here.

# Main view for displaying basic restaurant info
def main(request):
    return render(request, 'restaurant/main.html')

# Order view, includes daily special
def order(request):

    template_name = 'restaurant/order.html'

    # Define daily specials
    daily_specials = [
        {"name": "Seafood Paella ($19.99)"},
        {"name": "Vegetable Stir-Fry ($11.99)"},
        {"name": "Steak Frites ($24.99)"},
    ]
    
    # Select a random daily special
    daily_special = random.choice(daily_specials)

    context = {
        "daily_special": daily_special["name"],
    }

    return render(request, template_name, context)

# Confirmation view, handles form data
def confirmation(request):
    if request.method == 'POST':
        # Get order details from POST data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        items_ordered = request.POST.getlist('items')

        # Calculate total price and ready time
        prices = {'Pizza': 12, 'Burger': 10, 'Pasta': 8, 'Salad': 6}
        total_price = sum([prices[item] for item in items_ordered])

        ready_time = random.randint(30, 60)  # ready in 30-60 minutes

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'items_ordered': items_ordered,
            'total_price': total_price,
            'ready_time': ready_time,
        }

        return render(request, 'restaurant/confirmation.html', context)