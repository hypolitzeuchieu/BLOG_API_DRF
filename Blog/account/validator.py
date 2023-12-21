from rest_framework import serializers
from django.contrib.auth.models import User


def validate_username(value):
    queryset = User.objects.filter(username__iexact=value)
    if queryset.exists():
        raise serializers.ValidationError(f"{value} is already exist")
    return value


def validate_email(value):
    queryset = User.objects.filter(email__iexact=value)
    if queryset.exists():
        raise serializers.ValidationError(f"{value} is already exist")
    return value
