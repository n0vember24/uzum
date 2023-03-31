from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelf(BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj == request.user


class IsOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.user.is_authenticated and request.user.is_vendor or obj.owner == request.user.vendor


class IsVendor(BasePermission):
	def has_permission(self, request, view):
		return request.user.is_vendor


class IsAllowed(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.user.is_authenticated and request.user == obj.user


class IsOwnerOrReadOnly(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_authenticated and request.user.is_vendor or obj.owner == request.user.vendor


class IsVendorOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_authenticated and request.user.is_vendor


class IsAdminOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		return request.method in SAFE_METHODS or request.user.is_staff


class IsAdminOrOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.method in SAFE_METHODS or request.user == obj.owner or request.user.is_staff


class IsAdminOrVendor(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_authenticated and request.user.is_vendor or request.user.is_staff


class IsAdminOrSelf(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.user.is_authenticated and request.user.is_staff or request.user == obj


class IsNotAuthenticated(BasePermission):
	def has_permission(self, request, view):
		return not request.user.is_authenticated


class DenyAny(BasePermission):
	def has_permission(self, request, view):
		return False
