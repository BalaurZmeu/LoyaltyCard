from django.shortcuts import render
from .models import Card
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """View function for the home page of site."""
    return render(request, 'card_manager/index.html')


class CardListView(LoginRequiredMixin, generic.ListView):
    """Class-based view for all the cards."""
    model = Card
    paginate_by = 30


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    """Class-based view for the specific card."""
    model = Card


def generator(request):
    """View function for the card generator."""
    return render(request, 'card_manager/generator.html')

