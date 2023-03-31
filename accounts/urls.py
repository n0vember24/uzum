from django.urls import path

from uzum.views import CartView, FavouriteView, OrderView
from .views import GetMeView, UserRegisterView, ConfirmView, ChangePassword, TokenView, UserLoginView, UserLogoutView

urlpatterns = [
	# Me
	path('me/', GetMeView.as_view()),
	path('me/cart/', CartView.as_view({'get': 'list', 'post': 'create'})),
	path('me/cart/<int:pk>', CartView.as_view({'delete': 'destroy'})),
	path('me/favourites/', FavouriteView.as_view({'get': 'list', 'post': 'create'})),
	path('me/favourites/<int:pk>', FavouriteView.as_view({'delete': 'destroy'})),
	path('me/orders/', OrderView.as_view({'get': 'list', 'post': 'create'})),
	path('me/orders/<int:pk>', OrderView.as_view({'put': 'partial_update', 'get': 'retrieve'})),
	path('me/token/', TokenView.as_view()),
	path('me/change-password/', ChangePassword.as_view()),
	# Auth
	path('login/', UserLoginView.as_view()),
	path('register/', UserRegisterView.as_view()),
	path('register/confirm/', ConfirmView.as_view()),
	path('register/resend/', UserRegisterView.as_view()),
	path('logout/', UserLogoutView.as_view()),
]
