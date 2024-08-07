from django.shortcuts import get_object_or_404, render, redirect
from .models import Card, Purchase
from .forms import CardSearchForm, ActivateForm, CardGeneratorForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


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


class CardDetailView(PermissionRequiredMixin, generic.DetailView):
    """Class-based view for the specific card."""
    model = Card
    permission_required = 'card_manager.change_card'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_list'] = Purchase.objects.filter(card=self.object)
        context['form'] = ActivateForm(self.request.POST)
        return context

    def post(self, request, *args, **kwargs):
        if 'activate' in request.POST:
            return self.activate(request, *args, **kwargs)
        elif 'deactivate' in request.POST:
            return self.deactivate(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def activate(self, request, *args, **kwargs):
        card = self.get_object()
        form = ActivateForm(request.POST)
        if form.is_valid():
            expires_choice = form.cleaned_data['expires']
            card.expires = timezone.make_aware(
                datetime.now() + timedelta(days=int(expires_choice)))
            card.status = 'a'
            card.save()
        return redirect('card-detail', pk=card.pk)

    def deactivate(self, request, *args, **kwargs):
        card = self.get_object()
        card.status = 'n'
        card.save()
        return redirect('card-detail', pk=card.pk)


class CardDelete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Card
    success_url = reverse_lazy('card-list')
    permission_required = 'card_manager.delete_card'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("card-delete", kwargs={"pk": self.object.pk})
            )


class CardGeneratorView(SuccessMessageMixin, PermissionRequiredMixin, generic.edit.FormView):
    """Class-based view for the card generator."""
    template_name = 'card_manager/generator.html'
    form_class = CardGeneratorForm
    permission_required = 'card_manager.add_card'
    success_url = 'success'

    def form_valid(self, form):
        new_series = form.cleaned_data['series']
        expires_choice = form.cleaned_data['expires']
        number_of_cards = form.cleaned_data['quantity']
        self.generate_cards(new_series, expires_choice, number_of_cards)
        messages.success(self.request, f'Successfully generated {number_of_cards} cards.')
        return super().form_valid(form)

    def generate_cards(self, new_series, expires_choice, number_of_cards):
        exp_date = timezone.make_aware(
            datetime.now() + timedelta(days=int(expires_choice)))
        for i in range(number_of_cards):
            card = Card.objects.create(
                series = new_series,
                expires = exp_date)
            card.save()


@login_required
def success(request):
    """View function for the success page showed when 
    successfuly generated cards."""
    return render(request, 'card_manager/success.html')

