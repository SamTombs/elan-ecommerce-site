from django.urls import path
from .views import (
    BasketView,
    AddToBasketView,
    UpdateBasketItemView,
    RemoveFromBasketView,
)

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('add/', AddToBasketView.as_view(), name='add_to_basket'),
    path('items/<int:item_id>/', UpdateBasketItemView.as_view(), name='update_basket_item'),
    path('items/<int:item_id>/remove/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
]
