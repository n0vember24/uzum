from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
	DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilter
from .models import Vendor, Category, Product, ProductImage, Report
from .permissions import IsOwner, IsOwnerOrReadOnly, IsAdminOrVendor, IsAllowed
from .serializers import (
	VendorSerializer, CategorySerializer, ProductSerializer, ProductImageSerializer, CartSerializer,
	FavouriteSerializer, OrderSerializer, ReportSerializer
)


class CachedListAPIView(ListAPIView):
	@method_decorator(cache_page(60 * 15))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class VendorView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
	queryset = Vendor.objects.all()
	serializer_class = VendorSerializer
	permission_classes = IsOwnerOrReadOnly


class CategoryView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
	queryset = Category.objects.order_by('level')
	serializer_class = CategorySerializer
	permission_classes = IsAdminOrVendor,

	@method_decorator(cache_page(60 * 30))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class ProductView(ModelViewSet):
	queryset = Product.objects.order_by('-created_at')
	permission_classes = IsOwnerOrReadOnly,
	serializer_class = ProductSerializer
	filter_backends = DjangoFilterBackend, SearchFilter, OrderingFilter
	filterset_class = ProductFilter
	search_fields = 'title', 'category'
	ordering_fields = 'created_at', 'price'

	@method_decorator(cache_page(600))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user.vendor)


class VendorProductView(CachedListAPIView):
	serializer_class = ProductSerializer
	filter_backends = DjangoFilterBackend, SearchFilter, OrderingFilter
	filterset_class = ProductFilter
	search_fields = 'title', 'category__name'
	ordering_fields = 'created_at', 'price'

	def get_queryset(self):
		queryset = Product.objects.filter(owner_id=self.kwargs.get('pk'))
		return queryset


class ProductImageView(CachedListAPIView):
	serializer_class = ProductImageSerializer
	permission_classes = IsOwner,

	@method_decorator(cache_page(600))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		queryset = ProductImage.objects.filter(product_id=pk)
		return queryset


class ProductImageUpdateDestroyView(UpdateAPIView, DestroyAPIView):
	"""
	Mahsulot rasmini o'zgartirish yoki o'chrish uchun
	To'g'ri foydalanish uchun formahar xil rasm yuklaydigan formalardan foydalaning
	"""
	serializer_class = ProductImageSerializer
	permission_classes = IsOwner,

	def get_queryset(self):
		queryset = ProductImage.objects.filter(pk=self.kwargs.get('pk'))
		return queryset


class CategoryProductsView(ListModelMixin, GenericViewSet):
	serializer_class = ProductSerializer
	filter_backends = DjangoFilterBackend, SearchFilter, OrderingFilter
	filterset_class = ProductFilter
	search_fields = 'title', 'category__name'
	ordering_fields = 'created_at', 'price'

	def get_queryset(self):
		queryset = Product.objects.filter(category_id=self.kwargs.get('pk'))
		return queryset

	@method_decorator(cache_page(60 * 15))
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class CartView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
	serializer_class = CartSerializer
	permission_classes = IsAllowed,

	def create(self, request, *args, **kwargs):
		product = request.data.get('product')
		count = request.data.get('count')
		if product and str(count):
			if count < 1:
				return Response({'detail': "Mahsulotlar soni 1 dan kichik bo'lishi mumkin emas."}, HTTP_400_BAD_REQUEST)
			return super().create(request, *args, **kwargs)
		return Response({'detail': 'Fields: [product, count] are required.'}, HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return self.request.user.cart_set.all()


class FavouriteView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
	serializer_class = FavouriteSerializer
	permission_classes = IsAllowed,

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return self.request.user.favourite_set.all()


class OrderView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
	serializer_class = OrderSerializer
	permission_classes = IsAllowed,

	def update(self, request, *args, **kwargs):
		request.data.pop('cost')
		request.data.pop('products')
		request.data.pop('branch_point')
		return super().update(request, *args, **kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return self.request.user.order_set.all()


class ReportView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
	serializer_class = ReportSerializer
	queryset = Report.objects.filter()
