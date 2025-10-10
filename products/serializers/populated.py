from .common import ProductSerializer
from jwt_auth.serializers import UserSerializer
from reviews.serializers.populated import PopulatedReviewSerializer

class PopulatedProductSerializer(ProductSerializer):
    owner = UserSerializer()
    populated_reviews = PopulatedReviewSerializer(many=True)

