from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from src.apps.user.views import (
    RegisterView,
    LoginView,
    UserConfirmationView,
    VerifyEmail,
)


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/', VerifyEmail.as_view(), name="verify"),
    path('corfirm-self/', UserConfirmationView.as_view()),
]
