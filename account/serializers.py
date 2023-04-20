from django.contrib.auth import get_user_model

from .models import CustomUser
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import RevokedToken

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = CustomUser(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Пароли должны совпадать.'})
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)
    default_error_messages = {
        'bad_code': _('Link is expired or invalid!')
    }

    def validate(self, attrs):
        self.code = attrs['code']
        return attrs

    def save(self, **kwargs):
        try:
            user = CustomUser.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()
        except CustomUser.DoesNotExist:
            self.fail('bad_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        try:
            token = RefreshToken(self.token)
            user_id = token.payload["user_id"]
            user = User.objects.get(id=user_id)
            attrs['user'] = user
        except TokenError:
            raise serializers.ValidationError("Токен недействителен или истек.")
        return attrs

    def save(self, **kwargs):
        try:
            # token = RefreshToken(self.token)
            user = self.validated_data['user']
            if RevokedToken.objects.filter(token=self.token).exists():
                raise serializers.ValidationError("Токен уже отозван.")
            RevokedToken.objects.create(user=user, token=self.token)
        except TokenError as e:
            raise serializers.ValidationError(str(e))
