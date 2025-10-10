from django.urls import path
from .views import (
    BasketView,
    AddToBasketView,
    UpdateBasketItemView,
    RemoveFromBasketView,
    ClearBasketView
)

urlpatterns = [
    # Get basket
    path('', BasketView.as_view(), name='basket'),
    
    # Add item to basket
    path('add/', AddToBasketView.as_view(), name='add_to_basket'),
    
    # Update basket item quantity
    path('items/<int:item_id>/', UpdateBasketItemView.as_view(), name='update_basket_item'),
    
    # Remove item from basket
    path('items/<int:item_id>/remove/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    
    # Clear entire basket
    path('clear/', ClearBasketView.as_view(), name='clear_basket'),
]
