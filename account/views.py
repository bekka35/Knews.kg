from rest_framework import permissions

from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers
from .send_mail import send_confirmation_email

from django.contrib.auth import get_user_model

from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import LogoutSerializer

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print("USER ACT VALID=>", user.activation_code)
        if user:
            try:
                send_confirmation_email(user.email, user.activation_code)
            except User.DoesNotExist:
                return Response({'msg': 'Registered, but troubles with email!', 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class ActivationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ActivationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully activated!', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            serializer.save()
            return Response({"Сообщение": "Вы успешно вышли из системы.", "Пользователь": user.email},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
