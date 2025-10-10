from rest_framework import serializers
from .models import Product
from jwt_auth.serializers import UserSerializer
from reviews.serializers.populated import PopulatedReviewSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    populated_reviews = PopulatedReviewSerializer(many=True)