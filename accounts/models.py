from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import TextChoices, CharField, DateField, Model, CASCADE, DateTimeField, OneToOneField
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator(RegexValidator):
	regex = r"[0-9]{9}"


class VerifyCodeValidator(RegexValidator):
	regex = r'[0-9]{4}'


class User(AbstractUser):
	class Genders(TextChoices):
		MALE = 'male', _('male')
		FEMALE = 'female', _('female')
	
	class Types(TextChoices):
		VENDOR = 'vendor', _('vendor')
		CLIENT = 'client', _('client')
	
	username_validator = PhoneNumberValidator()
	username = CharField(
			_("phone number"),
			max_length=9,
			unique=True,
			help_text=_('Required. 9 characters. E.g.: XXXXXXXXX (X - number)'),
			validators=[username_validator],
			error_messages={"unique": _("A user with that phone number already exists."), },
	)
	type = CharField(
			_('type of user'),
			max_length=10,
			choices=Types.choices,
			default=Types.CLIENT,
			help_text='Type Of User(Vendor or Client)'
	)
	gender = CharField(
			_('gender'),
			max_length=6,
			choices=Genders.choices,
			default=None,
			help_text='Optional. Gender of User.',
			null=True,
			blank=True)
	birthday = DateField(_('birthday'), null=True, blank=True)
	
	class Meta:
		swappable = "AUTH_USER_MODEL"
		db_table = 'auth_user'
	
	@property
	def is_vendor(self):
		return self.type == 'vendor'


class VerifyCode(Model):
	code_validator = VerifyCodeValidator()
	user = OneToOneField(User, CASCADE)
	code = CharField(max_length=4, validators=[code_validator])
	time = DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = 'auth_verify_code'
	
	def __str__(self):
		return self.user
