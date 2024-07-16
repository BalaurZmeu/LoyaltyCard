from django.shortcuts import render
from .models import Card
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """View function for the home page of site."""
    context = {}
    return render(request, 'card_manager/index.html', context=context)


class CardListView(LoginRequiredMixin, generic.ListView):
    """Class-based view for all the cards."""
    model = Card
    paginate_by = 30


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    """Class-based view for the specific card."""
    model = Card

