from django.shortcuts import get_object_or_404, render, redirect
from .models import Card, Purchase
from .forms import CardSearchForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    """View function for the home page of site."""
    return render(request, 'card_manager/index.html')


class CardListView(LoginRequiredMixin, generic.ListView):
    """Class-based view for all the cards."""
    model = Card
    template_name = 'card_list.html'
    context_object_name = 'card_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CardSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['series']:
                queryset = queryset.filter(series__icontains=form.cleaned_data['series'])
            if form.cleaned_data['id_number']:
                queryset = queryset.filter(id_number__icontains=form.cleaned_data['id_number'])
            if form.cleaned_data['issued']:
                queryset = queryset.filter(issued__date=form.cleaned_data['issued'])
            if form.cleaned_data['expires']:
                queryset = queryset.filter(expires__date=form.cleaned_data['expires'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        for card in queryset:
            card.check_if_expired()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CardSearchForm(self.request.GET)
        return context


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    """Class-based view for the specific card."""
    model = Card
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_list'] = Purchase.objects.filter(card=self.object)
        return context


@login_required
def deactivate(request, pk):
    """Deactivate card."""
    card = get_object_or_404(Card, pk=pk)
    card.status = 'n'
    card.save()
    return redirect('card-detail', pk=pk)


@login_required
def generator(request):
    """View function for the card generator."""
    return render(request, 'card_manager/generator.html')

