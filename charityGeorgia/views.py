from django.shortcuts import render
from django.views.generic import TemplateView
from .scraper import scrape_and_cache_data
from .models import Charity

class CharityView(TemplateView):
    template_name = 'charity_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['charity_data'] = scrape_and_cache_data()
        context['charities'] = Charity.objects.exclude(name='ჰუმანიტარული კავშირი  კათარზისი')
        return context
