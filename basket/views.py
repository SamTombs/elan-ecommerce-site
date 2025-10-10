from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Basket, BasketItem
from .serializers import (
    BasketSerializer, 
    BasketItemSerializer, 
    AddToBasketSerializer, 
    UpdateBasketItemSerializer
)
from products.models import Product

class BasketView(APIView):
    """
    View to get the current user's basket
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get the user's basket with all items"""
        basket, created = Basket.objects.get_or_create(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToBasketView(APIView):
    """
    View to add items to the basket
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add a product to the basket or update quantity if already exists"""
        serializer = AddToBasketSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Get or create basket for user
            basket, created = Basket.objects.get_or_create(user=request.user)
            
            # Get the product
            product = get_object_or_404(Product, id=product_id)
            
            # Check if item already exists in basket
            basket_item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Item already exists, update quantity
                basket_item.quantity += quantity
                basket_item.save()
            
            # Return updated basket
            basket_serializer = BasketSerializer(basket)
            return Response(basket_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateBasketItemView(APIView):
    """
    View to update the quantity of a basket item
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, item_id):
        """Update the quantity of a specific basket item"""
        serializer = UpdateBasketItemSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            
            # Get the basket item (ensuring it belongs to the current user)
            basket_item = get_object_or_404(
                BasketItem, 
                id=item_id, 
                basket__user=request.user
            )
            
            basket_item.quantity = quantity
            basket_item.save()
            
            # Return updated basket
            basket_serializer = BasketSerializer(basket_item.basket)
            return Response(basket_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromBasketView(APIView):
    """
    View to remove items from the basket
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, item_id):
        """Remove a specific item from the basket"""
        # Get the basket item (ensuring it belongs to the current user)
        basket_item = get_object_or_404(
            BasketItem, 
            id=item_id, 
            basket__user=request.user
        )
        
        basket = basket_item.basket
        basket_item.delete()
        
        # Return updated basket
        basket_serializer = BasketSerializer(basket)
        return Response(basket_serializer.data, status=status.HTTP_200_OK)

class ClearBasketView(APIView):
    """
    View to clear all items from the basket
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        """Remove all items from the user's basket"""
        try:
            basket = Basket.objects.get(user=request.user)
            basket.items.all().delete()
            
            # Return empty basket
            basket_serializer = BasketSerializer(basket)
            return Response(basket_serializer.data, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response(
                {'message': 'Basket not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
