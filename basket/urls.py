from django.urls import path
from .views import (
    BasketView,
    AddToBasketView,
    UpdateBasketItemView,
    RemoveFromBasketView,
)

urlpatterns = [
    path('', BasketView.as_view()),
    path('add/', AddToBasketView.as_view()),
    path('items/<int:item_id>/', UpdateBasketItemView.as_view()),
    path('items/<int:item_id>/remove/', RemoveFromBasketView.as_view()),
]
