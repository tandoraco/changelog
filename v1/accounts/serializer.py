from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from v1.accounts import models as account_models
from v1.accounts.constants import PASSWORD_INCORRECT, CHANGELOG_TERMINOLOGY
from v1.accounts.utils import hash_password, verify_password
from v1.accounts.validators import password_validator


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, max_length=100, validators=[
            UniqueValidator(
                queryset=account_models.User.objects.all())])
    name = serializers.CharField(required=True, max_length=200)
    password = serializers.CharField(
        required=True, validators=[password_validator])

    def create(self, validated_data):
        password_hash = hash_password(validated_data.pop("password"))
        validated_data['password_hash'] = password_hash
        return account_models.User.objects.create(**validated_data)


class CompanySerializer(UserSerializer):
    company_name = serializers.CharField(max_length=100, required=True)
    website = serializers.URLField(max_length=200, required=True, validators=[
        UniqueValidator(account_models.Company.objects.all())
    ])
    changelog_terminology = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        company_name = validated_data.pop("company_name")
        website = validated_data.pop("website")
        changelog_terminology = validated_data.pop("changelog_terminology", CHANGELOG_TERMINOLOGY)
        user = super(CompanySerializer, self).create(validated_data)
        if user.pk:
            admin = account_models.Company.objects.create(admin=user, company_name=company_name, website=website,
                                                          changelog_terminology=changelog_terminology)
            return admin


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(
        required=True, validators=[password_validator])

    def validate(self, data):
        user = get_object_or_404(account_models.User, email=data['email'])

        if not verify_password(
                user=user, password=data['password']):
            raise ValidationError(PASSWORD_INCORRECT)

        return data
