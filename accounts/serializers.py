from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from accounts.models import User, VerifyCode


class UserSerializer(ModelSerializer):
	phone_number = CharField(source='username', validators=[User.username_validator], max_length=128, read_only=True)
	
	class Meta:
		model = User
		exclude = 'username', 'password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions'
		read_only_fields = 'is_staff', 'is_active', 'type'


class AuthUserSerializer(ModelSerializer):
	phone_number = CharField(source='username')
	
	class Meta:
		model = User
		fields = 'phone_number', 'password'
		write_only_fields = 'password',


class ChangePasswordSerializer(ModelSerializer):
	new_password = CharField(max_length=128)
	
	class Meta:
		model = User
		fields = 'password', 'new_password'
		write_only_fields = 'password', 'new_password'


class CodeSerializer(ModelSerializer):
	phone_number = CharField(source='user.username')
	
	class Meta:
		model = VerifyCode
		fields = 'phone_number', 'code'
