from django.http import Http404
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import Card, User


# Create your views here.
def index(request):
    num_cards = Card.objects.all().count()
    num_users = User.objects.all().count()
    open_cards = Card.objects.filter(card_status='OP').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cards': num_cards,
        'num_users': num_users,
        'open_cards': open_cards,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class CardListView(generic.ListView):
    model = Card
    paginate_by = 10


class CardDetailView(generic.DetailView):
    model = Card

    def card_detail_view(request, primary_key):
        try:
            book = Card.objects.get(pk=primary_key)
        except Card.DoesNotExist:
            raise Http404('Book does not exist')

        return render(request, 'user/card_detail.html', context={'card': Card})


class OwnedCardsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Card
    template_name = 'user/card_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Card.objects.filter(owner_id=self.request.user).filter(card_status__exact='OP').order_by('date_of_issue')