from rest_framework import permissions
from .permisions import is_household_member


class device_mixin():
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, is_household_member]
    