from random import randint

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from accounts.models import User, VerifyCode


def send_verification_code(phone_number):
	try:
		user = User.objects.get(username=phone_number)
		confirmation_code = str(randint(1000, 9999))
		VerifyCode.objects.create(user=user, code=confirmation_code)
		
		client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
		body = f"Sizning tasdiqlash kodingiz: {confirmation_code}"
		
		message = client.messages.create(f'+998{phone_number}', from_=settings.TWILIO_PHONE_NUMBER, body=body)
		return message
	except User.DoesNotExist:
		return None
	except TwilioRestException:
		return None
