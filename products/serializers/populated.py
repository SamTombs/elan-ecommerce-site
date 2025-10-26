from .common import ProductSerializer
from reviews.serializers.populated import PopulatedReviewSerializer

class PopulatedProductSerializer(ProductSerializer):
    populated_reviews = PopulatedReviewSerializer(many=True)

