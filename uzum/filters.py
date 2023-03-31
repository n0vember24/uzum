from django_filters import FilterSet, NumberFilter, CharFilter

from .models import Product


class ProductFilter(FilterSet):
	category = CharFilter(field_name='category__name', lookup_expr='icontains')
	
	class Meta:
		model = Product
		fields = {
			'price': ('gte', 'lte'),
		}
