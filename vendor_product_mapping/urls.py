from django.urls import path
from .views import VendorProductMappingListCreateAPIView, VendorProductMappingDetailAPIView

urlpatterns = [
    path('', VendorProductMappingListCreateAPIView.as_view(), name='vp-mapping-list-create'),
    path('<int:pk>/', VendorProductMappingDetailAPIView.as_view(), name='vp-mapping-detail'),
]
