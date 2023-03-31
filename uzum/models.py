from random import randint

from django.contrib.postgres.fields import ArrayField
from django.db.models import (
	Model, CharField, SlugField, SET_NULL, ImageField, DateField, ForeignKey, SmallIntegerField, DecimalField,
	TextField, CASCADE, DateTimeField, TextChoices, ManyToManyField, OneToOneField
)
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import User


class Vendor(Model):
	name = CharField(max_length=100)
	description = CharField(max_length=255, null=True, blank=True)
	logo = ImageField(upload_to='img/vendors/', blank=True)
	owner = OneToOneField(User, SET_NULL, null=True)
	slug = SlugField(max_length=255, unique=True, null=True, blank=True)
	register_date = DateField(auto_now_add=True)
	
	class Meta:
		ordering = '-register_date',
	
	def save(self, *args, **kwargs):
		self.owner.type = 'vendor'
		self.owner.save()
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	
	def delete(self, *args, **kwargs):
		if self.owner:
			self.owner.type = 'client'
			self.owner.save()
		super().delete(*args, **kwargs)
	
	def __str__(self):
		return self.name


class Category(MPTTModel):
	name = CharField(max_length=100)
	slug = SlugField(max_length=255, unique=True)
	parent = TreeForeignKey('self', SET_NULL, 'children', null=True, blank=True)
	
	class Meta:
		verbose_name_plural = 'Categories'
		ordering = 'pk',
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	
	def __str__(self):
		return self.name


class Product(Model):
	title = CharField(max_length=200)
	owner = ForeignKey(Vendor, SET_NULL, null=True)
	category = ForeignKey(Category, SET_NULL, null=True)
	count = SmallIntegerField()
	price = DecimalField(max_digits=6, decimal_places=2)
	details = ArrayField(CharField(max_length=200), null=True, blank=True)
	description = TextField()
	slug = SlugField(max_length=255, unique=True)
	created_at = DateTimeField(auto_now_add=True)
	updated_at = DateTimeField(auto_now=True)
	
	def save(self, *args, **kwargs):
		self.slug = f'{slugify(self.title)}-{randint(1000, 9999)}'
		super().save(*args, **kwargs)
	
	def __str__(self):
		return self.title


class ProductImage(Model):
	product = ForeignKey(Product, CASCADE)
	image = ImageField(upload_to='img/products')
	
	@property
	def owner(self):
		return self.product.owner
	
	def __str__(self):
		return self.product.title


class Cart(Model):
	user = ForeignKey(User, CASCADE)
	product = OneToOneField(Product, SET_NULL, null=True)
	count = SmallIntegerField()
	date = DateTimeField(auto_now=True)
	
	def __str__(self):
		return f'{self.product.title}({self.count}) -> {self.user.username}'


class Favourite(Model):
	user = ForeignKey(User, CASCADE)
	product = OneToOneField(Product, CASCADE)
	date = DateTimeField(auto_now=True)
	
	def __str__(self):
		return f'{self.product.title} -> {self.user.username}'


class Report(Model):
	vendor = ForeignKey(Vendor, SET_NULL, null=True)
	products = ManyToManyField(Product)
	date = DateTimeField(auto_now_add=True)
	
	@property
	def products_count(self):
		return self.products.all().count()
	
	def __str__(self):
		return self.vendor.name


class BranchPoint(Model):
	address = CharField(max_length=255)
	
	def __str__(self):
		return self.address


class Order(Model):
	class Statuses(TextChoices):
		WAIT_PAYMENT = 'wait-payment', _('wait payment')
		COLLECTING = 'collecting', _('collecting')
		DELIVERING = 'delivering', _('delivering')
		PICK_UP = 'pick-up', _('you can pick up')
		DONE = 'done', _('issued to the buyer')
		RETURNED = 'returned', _('returned')
	
	user = ForeignKey(User, SET_NULL, null=True)
	status = CharField(max_length=50, choices=Statuses.choices, default=Statuses.COLLECTING)
	order_date = DateTimeField(auto_now_add=True)
	delivery_date = DateField(null=True, blank=True)
	branch_point = ForeignKey(BranchPoint, SET_NULL, null=True)
	cost = DecimalField(max_digits=9, decimal_places=2)
	products = ManyToManyField(Product)
	
	def __str__(self):
		return f'{self.id} -> {self.user.username}'
