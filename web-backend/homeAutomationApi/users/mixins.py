from .permissions import is_household_member
from rest_framework import permissions


class users_mixin():
    permission_classes = [permissions.IsAuthenticated, is_household_member]