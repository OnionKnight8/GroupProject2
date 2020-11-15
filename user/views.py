from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login
from user.models import Card, Customer
from .forms import ExtendedUserCreationForm, CustomerForm, TransactionForm


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
            raise Http404('Card does not exist')

        return render(request, 'user/card_detail.html', context={'card': Card})


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        form.fields['card_id'].queryset = Card.objects.filter(owner_id=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            atm_machine = instance.machine_id
            customer = request.user.customer
            if instance.card_id.is_expired:
                instance.transaction_status = 'CA'
                instance.response_code = 54
                instance.save()
            else:
                if instance.transaction_type == 'DE':
                    customer.balance += instance.transaction_amount
                    customer.save()
                    atm_machine.current_balance += instance.transaction_amount
                    atm_machine.save()
                elif instance.transaction_type == 'WI':
                    if atm_machine.current_balance >= instance.transaction_amount and customer.balance >= instance.transaction_amount:
                        customer.balance -= instance.transaction_amount
                        customer.save()
                        atm_machine.current_balance -= instance.transaction_amount
                        atm_machine.save()
                    else:
                        instance.transaction_status = 'CA'
                        instance.response_code = 51
                        instance.save()

            return HttpResponseRedirect('/user') # todo: change to transaction history
    else:
        form = TransactionForm()
        form.fields['card_id'].queryset = Card.objects.filter(owner_id=request.user)
    return render(request, 'user/transaction.html', {'form': form, })

