
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from .models import Product
from .serializers.common import ProductSerializer

class CategoryProductListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, category):
        # Validate category
        valid_categories = ['lift', 'explore', 'vault']
        if category not in valid_categories:
            return Response(
                {'error': 'Invalid category'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = Product.objects.filter(category=category)
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, ) # sets the permission levels of the specific view by passing in the rest framework authentication class

    # custom method to retrieve a product from the DB and error if it's not found
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Can't find that product") # <-- import the NotFound exception from rest_framwork.exceptions


