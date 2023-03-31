from django.contrib import admin

from .models import Vendor, Product, Category, ProductImage, Report, Cart, Favourite, Order, BranchPoint

admin.site.register((ProductImage, Cart, Favourite, Order, Report, BranchPoint))


@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
	list_display = 'name', 'owner'
	search_fields = 'name', 'owner__username', 'owner__phone_number'
	list_filter = 'register_date',
	ordering = 'name',
	readonly_fields = 'slug', 'register_date'


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
	readonly_fields = 'slug',
	search_fields = 'name',


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = 'title', 'owner'
	readonly_fields = 'slug',
	search_fields = 'title', 'category'
	sortable_by = 'price', 'count'
	list_filter = 'created_at', 'updated_at'
