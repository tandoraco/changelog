from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from v1.accounts.models import Company


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        try:
            get_object_or_404(Company, admin=request.user)
            return True
        except Http404:
            return False
