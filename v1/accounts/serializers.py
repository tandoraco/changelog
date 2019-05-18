from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from v1.accounts import models as account_models
from v1.accounts.constants import PASSWORD_INCORRECT, CHANGELOG_TERMINOLOGY, EMAIL_NOT_FOUND, RESET_TOKEN_INVALID
from v1.accounts.models import ForgotPassword, User
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


class ForgotPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForgotPassword
        fields = '__all__'

    def validate(self, data):
        email = data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(EMAIL_NOT_FOUND)

        return data


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(required=True, validators=[password_validator])

    def validate(self, data):
        token = data.get('token')

        try:
            ForgotPassword.objects.get(token=token)
        except ForgotPassword.DoesNotExist:
            raise serializers.ValidationError(RESET_TOKEN_INVALID)

        return data

    def create(self, validated_data):
        token = validated_data.pop('token')
        password_hash = hash_password(validated_data.pop('password'))

        forgot_password = ForgotPassword.objects.get(token=token)
        user = User.objects.get(email=forgot_password.email)
        user.password_hash = password_hash
        user.save()

        # after successful reset of password, delete the token
        forgot_password.delete()
        return user
