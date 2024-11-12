from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result 

# Create your views here.
class ResultsListView(ListView): 
    '''View to show a list of result'''

    template_name = 'marathon_analytics/results.html'
    model = Result 
    context_object_name = 'results'
    paginate_by = 50

    def get_queryset(self): 
        '''Limit the results to  small number of records'''

        # default queryset is all of the records: 
        qs = super().get_queryset()

        # return qs[:25] # limit to 25 records

        # handle search form/URL parameters: 
        if 'city' in self.request.GET:
            city = self.request.GET['city']

            # filter the Results by this parameter 
            qs = Result.objects.filter(city__icontains=city) # i  is for case sensitivity 

        return qs

class ResultDetailView(DetailView):
    '''Display a single Result on it's own page'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result 
    context_object_name = "r"

    # implement some methods ...
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = content['r']

        # get data: half=marathon splits 
        first_half_seconds = (r.time_half1.hour *3600 + 
                              r.time_half1.minute * 60 + 
                              r.time_half1.second)
        
        second_half_seconds = (r.time_half2.hour *3600 + 
                              r.time_half2.minute * 60 + 
                              r.time_half2.second)

        # # build a pie chart 
        # X = ['first half seconds', 'second half seconds']
        # y = [first_half_seconds, second_half_seconds]
        # print(f'x={x})
        # print(f'y={y}'')
        # # add the pie chart to the context


