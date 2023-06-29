from django.urls import include, path
from django.views.generic import RedirectView

from .views import (
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomUserDetailsView,
)

urlpatterns = [
    path("auth/user/", CustomUserDetailsView.as_view(), name="user_details"),
    path(
        "auth/password/change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "auth/password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path(
        "accounts/profile/<int:pk>",
        RedirectView.as_view(url="/", permanent=True),
        name="profile-redirect",
    ),
]
