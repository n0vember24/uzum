from django.contrib.auth import login, authenticate, logout
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
	HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from uzum.permissions import IsNotAuthenticated, IsSelf
from .models import User, VerifyCode
from .serializers import AuthUserSerializer, CodeSerializer, ChangePasswordSerializer, UserSerializer
from .shortcuts import send_verification_code


class GetMeView(RetrieveAPIView, UpdateAPIView):
	serializer_class = UserSerializer
	permission_classes = IsSelf,
	
	def get_queryset(self):
		return self.request.user
	
	def get_object(self):
		return self.get_queryset()


class UserLoginView(CreateAPIView):
	"""
	Login with CSRF Token(Cookie)
	"""
	queryset = User.objects
	serializer_class = AuthUserSerializer
	permission_classes = IsNotAuthenticated,
	
	def post(self, request, *args, **kwargs):
		try:
			phone_number = request.data.get('phone_number')
			password = request.data.get('password')
			if phone_number and password:
				user = authenticate(username=phone_number, password=password)
				if user:
					login(request, user)
					return Response({'detail': 'Successfully login.'})
				return Response({'detail': 'Login qilayotganda xatolik.'}, HTTP_500_INTERNAL_SERVER_ERROR)
			return Response({'detail': 'Fields: [phone_number, password] are required.'}, HTTP_400_BAD_REQUEST)
		except Exception as exc:
			return Response({'error': exc})


class UserRegisterView(CreateAPIView):
	queryset = User.objects
	serializer_class = AuthUserSerializer
	permission_classes = IsNotAuthenticated,
	
	def post(self, request, *args, **kwargs):
		phone_number = request.data.get('phone_number')
		password = request.data.get('password')
		print(type(phone_number), password)
		if phone_number and password:
			user = User.objects.filter(username=phone_number)
			if not user.exists():
				User.objects.create_user(phone_number, password=password, is_active=False)
				send_verification_code(phone_number)
				return Response({'success': 'SMS xabarlaringizni tekshiring'})
			elif user.exists():
				user = user.first()
				if not user.is_active:
					verify_code = VerifyCode.objects.filter(user=user)
					if verify_code.exists():
						verify_code.first().delete()
					send_verification_code(phone_number)
					return Response({'success': 'SMS xabarlaringizni tekshiring'})
				return Response({'active': 'Foydalanuvchi aktivlashtirilgan'}, HTTP_500_INTERNAL_SERVER_ERROR)
		return Response({'error': 'Barcha maydonlarni to\'ldiring'}, HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
	permission_classes = IsAuthenticated,
	
	def get(self, request):
		logout(request)
		return Response({'detail': 'Successfully logout.'})


class ConfirmView(CreateAPIView):
	permission_classes = IsNotAuthenticated,
	serializer_class = CodeSerializer
	
	def post(self, request, *args, **kwargs):
		try:
			phone_number = request.data.get('phone_number')
			confirm_code = request.data.get('code')
			if phone_number and confirm_code:
				user = User.objects.get(username=phone_number)
				if not user.is_active:
					verify_code = VerifyCode.objects.get(user=user)
					if verify_code.code == confirm_code:
						user.is_active = True
						user.save()
						refresh = RefreshToken.for_user(user)
						verify_code.delete()
						return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
					return Response({'error': "Noto'g'ri kod."}, HTTP_400_BAD_REQUEST)
				return Response({'active': 'Foydalanuvchi aktivlashtirilgan'}, HTTP_500_INTERNAL_SERVER_ERROR)
			return Response({'error': "Iltimos, barcha maydonlarni to'ldiring."}, HTTP_400_BAD_REQUEST)
		except User.DoesNotExist:
			msg = {'error': "Bunday foydalanuvchi bazada yo'q. Iltimos, ro'yxatda o'tqizing qaytadan urinib ko'ring."}
			return Response(msg, HTTP_404_NOT_FOUND)
		except VerifyCode.DoesNotExist:
			msg = {'error': "Sizga kod hali jo'natilmadi. Kuting yoki qaytadan urining."}
			return Response(msg, HTTP_400_BAD_REQUEST)


class ChangePassword(CreateAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = IsAuthenticated,
	
	def post(self, request, *args, **kwargs):
		user = request.user
		password = request.data.pop('password', None)
		new_password = request.data.pop('new_password', None)
		if user.check_password(password):
			if password != new_password:
				user.set_password(new_password)
				user.save()
				user = authenticate(username=user.username, password=new_password)
				login(request, user)
				return Response({'success': "Parol muvaffaqiyatli o'zgartirildi"})
			return Response({'detail': "Yangi parol eskisi bilan bir xil bo'la olmaydi"}, HTTP_400_BAD_REQUEST)
		return Response({'detail': "Parol noto'g'ri."}, HTTP_400_BAD_REQUEST)


class TokenView(APIView):
	permission_classes = IsAuthenticated,
	
	def get(self, request):
		refresh = RefreshToken.for_user(request.user)
		return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
