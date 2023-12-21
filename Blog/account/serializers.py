from rest_framework import serializers
from django.contrib.auth.models import User

from .validator import validate_username, validate_email


class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(validators=[validate_username])
    first_name = serializers.CharField()
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(style={'input_type': 'password'})

    def create(self, validated_data):
        username = self.validated_data.get('username')
        first_name = self.validated_data.get('first_name')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')

        return User.objects.create_user(username=username, first_name=first_name, email=email, password=password)
