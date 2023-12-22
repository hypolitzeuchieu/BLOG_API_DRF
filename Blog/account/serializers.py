from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from .validator import validate_username, validate_email


class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(validators=[validate_username])
    first_name = serializers.CharField()
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        username = self.validated_data.get('username')
        first_name = self.validated_data.get('first_name')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')

        return User.objects.create_user(username=username, first_name=first_name, email=email, password=password)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('account not found')
        return data

    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {'message': 'invalid credentials', 'data': {}}

        refresh = RefreshToken.for_user(user)

        return {'message': 'login success', 'data': {'token': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            }}}
