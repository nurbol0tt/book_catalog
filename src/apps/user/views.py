import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from src.apps.user.serializers import UserCreateSerializer
from src.apps.user.tasks import send_message_email

from apps.user.models import User

from src.apps.user.serializers import EmailVerificationSerializer, EmailConfirmSerializer
from src.core import settings


class RegisterView(APIView):
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, format=None) -> Response: # noqa
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserConfirmationView(APIView):
    serializer_class = EmailConfirmSerializer

    @swagger_auto_schema(request_body=EmailConfirmSerializer)
    def post(self, request, format=None) -> Response:  # noqa
        serializer = EmailConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data['email'])
        current_site = get_current_site(request).domain

        send_message_email.delay(email=user.email, current_site=current_site)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request) -> Response:
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_object_or_404(User, email=payload.get('email'))
            if not user.is_confirmed:
                user.is_confirmed = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    ...
