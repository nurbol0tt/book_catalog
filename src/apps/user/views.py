from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from src.apps.user.serializers import UserCreateSerializer
from src.apps.user.tasks import send_message_email


class RegisterView(APIView):
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, format=None) -> Response: # noqa
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ConfirmUserView(APIView):

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, format=None) -> Response: # noqa
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_message_email.delay(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    ...
