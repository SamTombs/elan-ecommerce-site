from django.urls import path
from .views import ProductDetailView, CategoryProductListView


urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view()),
    path('category/<str:category>/', CategoryProductListView.as_view()),
]
