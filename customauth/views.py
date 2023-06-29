from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    UserDetailsView,
)

from .serializers import (
    CustomLoginSerializer,
    CustomPasswordChangeSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomRegisterSerializer,
    CustomUserDetailsSerializer,
)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer


class CustomPasswordChangeView(PasswordChangeView):
    serializer_class = CustomPasswordChangeSerializer


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    serializer_class = CustomPasswordResetConfirmSerializer
