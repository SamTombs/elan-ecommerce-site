from rest_framework import serializers
from .models import Basket, BasketItem
from products.serializers import ProductSerializer

class BasketItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual basket items
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at', 'updated_at']
        read_only_fields = ['id', 'added_at', 'updated_at']
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

class BasketSerializer(serializers.ModelSerializer):
    """
    Serializer for the entire basket
    """
    items = BasketItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Basket
        fields = ['id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddToBasketSerializer(serializers.Serializer):
    """
    Serializer for adding items to basket
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_product_id(self, value):
        """Validate that the product exists"""
        from products.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")
        return value

class UpdateBasketItemSerializer(serializers.Serializer):
    """
    Serializer for updating basket item quantity
    """
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
