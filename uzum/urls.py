from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
	VendorView, CategoryView, CategoryProductsView, ProductView, VendorProductView, ProductImageView,
	ProductImageUpdateDestroyView
)

router = DefaultRouter()
router.register('vendors', VendorView)
router.register('categories', CategoryView)
router.register('products', ProductView)

urlpatterns = [
	path('', include(router.urls)),
	path('vendors/<int:pk>/products/', VendorProductView.as_view()),
	path('categories/<int:pk>/products/', CategoryProductsView.as_view({'get': 'list'})),
	path('products/<int:pk>/images/', ProductImageView.as_view()),
	path('products/images/<int:pk>/', ProductImageUpdateDestroyView.as_view()),
]
