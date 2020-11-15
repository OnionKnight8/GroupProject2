from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import authenticate, login
from user.models import Card
from django.contrib import messages
from .forms import ExtendedUserCreationForm, CustomerForm


# Create your views here.
# Asks user to log in on homepage.
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "not logged in"

    context = {'username': username}
    return render(request, 'index.html', context)

# todo: add user profile page


def register(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if form.is_valid() and customer_form.is_valid():
            user = form.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect('/user')
    else:
        form = ExtendedUserCreationForm()
        customer_form = CustomerForm()

    context = {'form': form, 'customer_form': customer_form}
    return render(request, 'user/register.html', context)


@login_required
def confirm_card(request):
    if request.method == 'POST':
        card = Card(owner_id=request.user)
        card.save()
        return HttpResponseRedirect('/user/cardconfirmed/')
    context = {}
    return render(request, 'user/confirmcard.html', context)


def confirmation_screen(request):
    context = {}
    return render(request, 'user/cardconfirmed.html', context)


# Shows cards owned by user when they are logged in.
class OwnedCardsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'user/card_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Card.objects.filter(owner_id=self.request.user).order_by('date_of_issue')


# Shows details about a specific ATM card.
class CardDetailView(generic.DetailView):
    model = Card

    def card_detail_view(request, primary_key):
        try:
            card = Card.objects.get(pk=primary_key)
        except Card.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'user/card_detail.html', context={'card': Card})


