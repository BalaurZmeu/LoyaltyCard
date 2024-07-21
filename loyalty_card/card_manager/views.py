from django.shortcuts import get_object_or_404, render, redirect
from .models import Card, Purchase
from .forms import CardSearchForm, ActivateForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
            if expires_choice == '1':
                card.expires = timezone.make_aware(datetime.now() + timedelta(days=30))
            elif expires_choice == '6':
                card.expires = timezone.make_aware(datetime.now() + timedelta(days=180))
            elif expires_choice == '12':
                card.expires = timezone.make_aware(datetime.now() + timedelta(days=365))
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


@login_required
def generator(request):
    """View function for the card generator."""
    return render(request, 'card_manager/generator.html')

