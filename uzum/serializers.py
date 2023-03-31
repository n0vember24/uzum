from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, RelatedField

from .models import Vendor, Category, Product, ProductImage, Cart, Favourite, Order, Report


class ImagesRelatedField(RelatedField):
	def to_representation(self, value):
		return str(value.image.url)


class VendorSerializer(ModelSerializer):
	class Meta:
		model = Vendor
		fields = '__all__'
		read_only_fields = 'slug', 'owner', 'register_date'


class CategorySerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'
		read_only_fields = 'slug',


class ProductSerializer(ModelSerializer):
	images = ImagesRelatedField(source='productimage_set', many=True, read_only=True)
	
	class Meta:
		model = Product
		fields = '__all__'
		read_only_fields = 'slug', 'created_at', 'updated_at', 'owner'


class ProductImageSerializer(ModelSerializer):
	class Meta:
		model = ProductImage
		fields = '__all__'
		read_only_fields = 'product',


class CartSerializer(ModelSerializer):
	user = HiddenField(default=CurrentUserDefault())
	
	class Meta:
		model = Cart
		fields = '__all__'


class FavouriteSerializer(ModelSerializer):
	user = HiddenField(default=CurrentUserDefault())
	
	class Meta:
		model = Favourite
		fields = '__all__'


class OrderSerializer(ModelSerializer):
	user = HiddenField(default=CurrentUserDefault())
	
	class Meta:
		model = Order
		fields = '__all__'


class ReportSerializer(ModelSerializer):
	class Meta:
		model = Report
		fields = '__all__'
