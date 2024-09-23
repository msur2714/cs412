## quotes/views.py
## Description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

# List of Quotes from Audrey Hepburn
QUOTES = ['The most important thing is to enjoy your life. To be happy. It’s all that matters.',
          'For beautiful eyes, look for the good in others; for beautiful lips, speak only words of kindness; and for poise, walk with the knowledge that you are never alone.',
          'Nothing is impossible; the word itself says ‘I’m possible!’']

# List of Images from Audrey Hepburn
IMAGES = ['https://cdn.britannica.com/48/77148-050-12B5CAD5/Audrey-Hepburn-Roman-Holiday.jpg', 
          'https://runwaymagazines.com/wp-content/uploads/audrey-hepburn-style-runway-magazine.jpeg', 
          'https://cdn.britannica.com/32/68032-050-26C49C30/Audrey-Hepburn-1955.jpg']


def home(request):
    '''
    Function to handle the URL request for /quotes (home page).
    Delegate rendering to the template quotes/home.html.
    '''
    # Use this template to render the response
    template_name = 'quotes/home.html'

    # Select a quote and image
    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "random_quote": selected_quote,
        "random_image": selected_image,
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /quotes/about (about page).
    Delegate rendering to the template quotes/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def quote(request):
    '''
    Function to handle the URL request for /quotes/quote (quote page).
    Delegate rendering to the template quotes/quote.html.
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'

    # Randomly select a quote and image
    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "random_quote": selected_quote,
        "random_image": selected_image,
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /quotes/show_all (show all page).
    Delegate rendering to the template quote/show_all.html.
    '''
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)