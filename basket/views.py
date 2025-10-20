from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Basket, BasketItem
from .serializers import (
    BasketSerializer,
    AddToBasketSerializer,
    UpdateBasketItemSerializer
)
from products.models import Product


class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        basket, created = Basket.objects.get_or_create(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToBasketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

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
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):

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
    permission_classes = [IsAuthenticated]
    def delete(self, request, item_id):

        # Get the basket item (ensuring it belongs to the current user
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

