from ..serializers import ReviewSerializer
from jwt_auth.serializers import UserSerializer

class PopulatedReviewSerializer(ReviewSerializer):
    owner = UserSerializer()