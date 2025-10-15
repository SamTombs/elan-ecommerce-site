
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from .models import Product
from .serializers.common import ProductSerializer



class ProductListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, _request):
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["owner"] = request.user.id
        product_to_add = ProductSerializer(data=request.data)
        if product_to_add.is_valid():
            product_to_add.save()
            return Response(product_to_add.data, status=status.HTTP_201_CREATED)
        return Response(product_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ProductDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, ) # sets the permission levels of the specific view by passing in the rest framework authentication class

    # custom method to retrieve a product from the DB and error if it's not found
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Can't find that product") # <-- import the NotFound exception from rest_framwork.exceptions

    def get(self, _request, pk):
        product = self.get_product(pk=pk)
        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product_to_update = self.get_product(pk=pk)
        if product_to_update.owner and product_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_product = ProductSerializer(product_to_update, data=request.data)
        if updated_product.is_valid():
            updated_product.save()
            return Response(updated_product.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_product.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        product_to_delete = self.get_product(pk=pk)

        if product_to_delete.owner and product_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        product_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)