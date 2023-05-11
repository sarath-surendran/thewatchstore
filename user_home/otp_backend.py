from django.contrib.auth.backends import ModelBackend
from .models import CustomUser as User

class PhoneOTPBackend(ModelBackend):
    def authenticate(self,request,phone=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            return user
            
        except User .DoesNotExist:
            return None