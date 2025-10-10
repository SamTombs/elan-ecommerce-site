from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework.exceptions import NotFound
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Review
from .serializers.common import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class ReviewListView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("CREATING REVIEW USER ID", request.user.id)
        request.data["owner"] = request.user.id
        review_to_add = ReviewSerializer(data=request.data)
        try:
            review_to_add.is_valid()
            review_to_add.save()
            return Response(review_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ReviewDetailView(APIView):
    permission_classes = (IsAuthenticated,) # only get here if you are signed in

    def get_review(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound(detail="Can't find that Review")

    def get(self, request, pk):
        review = self.get_review(pk=pk)
        serialized_review = ReviewSerializer(review)
        return Response(serialized_review.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        review_to_update = self.get_review(pk=pk)

        # request has been through the authentication process. It started as request.
        # request was sent with a token.
        #  token was checked, and the user was found.
        #  user was added to the request.
        if review_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_review = ReviewSerializer(review_to_update, data=request.data)

        if updated_review.is_valid():
            updated_review.save()
            return Response(updated_review.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_review.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, request, pk):
        review_to_delete = self.get_review(pk=pk)

        if review_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        review_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)