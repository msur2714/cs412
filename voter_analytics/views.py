from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.express as px
from datetime import datetime

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Filtering criteria for GET parameters
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('voter_score')
        voted_in_2020 = self.request.GET.get('v20state')
        voted_in_2022 = self.request.GET.get('v22general')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            min_dob_date = datetime.strptime(min_dob, '%Y').date()
            queryset = queryset.filter(date_of_birth__gte=min_dob_date)
        if max_dob:
            max_dob_date = datetime.strptime(max_dob, '%Y').date()
        if score:
            queryset = queryset.filter(voter_score=score)
        if voted_in_2020 is not None:
            queryset = queryset.filter(voted_in_2020=v20state)
        if voted_in_2022 is not None:
            queryset = queryset.filter(voted_in_2022=v22general)

        return queryset

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Filtering criteria for GET parameters
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('voter_score')
        voted_in_2020 = self.request.GET.get('v20state')
        voted_in_2022 = self.request.GET.get('v22general')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            # Convert to date format and compare year
            min_dob_date = datetime.strptime(min_dob, '%Y').date()
            queryset = queryset.filter(date_of_birth__gte=min_dob_date)
        if max_dob:
            # Convert to date format and compare year
            max_dob_date = datetime.strptime(max_dob, '%Y').date()
            queryset = queryset.filter(date_of_birth__lte=max_dob_date)
        if score:
            queryset = queryset.filter(voter_score=score)
        if voted_in_2020 is not None:
            queryset = queryset.filter(v20state=voted_in_2020)
        if voted_in_2022 is not None:
            queryset = queryset.filter(v22general=voted_in_2022)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        # Birth year distribution graph
        birth_years = queryset.values('date_of_birth__year')
        birth_year_count = {year: 0 for year in range(1900, 2025)} 
        
        # Count occurrences of each birth year
        for voter in birth_years:
            birth_year_count[voter['date_of_birth__year']] += 1
        
        # Histogram - Birth Year Distribution
        birth_years_graph = px.bar(
            x=list(birth_year_count.keys()),
            y=list(birth_year_count.values()),
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
            title="Voter Distribution by Year of Birth"
        )

        # Party affiliation distribution graph
        party_affiliations = queryset.values('party_affiliation')
        party_count = {}
        for party in party_affiliations:
            party_count[party['party_affiliation']] = party_count.get(party['party_affiliation'], 0) + 1
        
        party_graph = px.pie(
            names=list(party_count.keys()),
            values=list(party_count.values()),
            title="Voter Distribution by Party Affiliation"
        )

        # Election participation graph
        election_participation = {
            '2020': queryset.filter(v20state=True).count(),
            '2021': queryset.filter(v21town=True).count(),
            '2021 Primary': queryset.filter(v21primary=True).count(),
            '2022 General': queryset.filter(v22general=True).count(),
            '2023 Town': queryset.filter(v23town=True).count(),
        }

        election_graph = px.bar(
            x=list(election_participation.keys()),
            y=list(election_participation.values()),
            labels={'x': 'Election Year', 'y': 'Voter Participation'},
            title="Voter Participation in Elections"
        )

        context['birth_years_graph'] = birth_years_graph.to_html(full_html=False)
        context['party_graph'] = party_graph.to_html(full_html=False)
        context['election_graph'] = election_graph.to_html(full_html=False)

        return context