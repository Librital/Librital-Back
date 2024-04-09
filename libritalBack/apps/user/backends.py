from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario


class AuthenticateBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Usuario.objects.filter(email=email).first()
            if user is not None:
                if check_password(password, user.password):
                    return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
