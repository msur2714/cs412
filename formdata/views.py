from django.shortcuts import render

# Create your views here.

def show_form(request):
    '''Show the contact form.'''

    template_name = "formdata/form.html"

    return render(request, template_name)

def submit(request):
    '''
    Handle the form submission. 
    Read the form from the request, 
    and send it back to a template. 
    '''

    template_name = 'formdata/confirmation.html'
    # print(request)

    # Check that we have a POST request
    if request.POST:
        
        # read the form data into python variables 
        name = request.POST['name']
        favourite_colour = request.POST['favourite_colour']
        
        # package the form data up as context variables for the template
        context = {
            'name': name, 
            'favourite_colour': favourite_colour,
        }

        return render(request, template_name)
    
    # Handle GET request on this URL
    # an "ok" solution...
    # return HttpResponse("Nope.")

    # a better solution... 
    # template_name= "formdata/form.html"
    # return render(request, template_name)

    # a better yet solution: redirect to the correct URL: 
    return redirect("show_form")
