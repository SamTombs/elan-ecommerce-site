from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryProductListView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('category/<str:category>/', CategoryProductListView.as_view()),
]
