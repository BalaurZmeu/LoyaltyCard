from django.shortcuts import render
from .models import Card
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html', context=context)


class CardListView(LoginRequiredMixin, generic.ListView):
    model = Card
    paginate_by = 30


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    model = Card

