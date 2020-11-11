from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cards/', views.CardListView.as_view(), name='cards'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('mycards/', views.OwnedCardsByUserListView.as_view(), name='my-cards'),
]