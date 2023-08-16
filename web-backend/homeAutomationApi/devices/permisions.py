from rest_framework import permissions


class is_household_member(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.household == obj.household or not obj.household or request.user.isadmin:
            return True
        return False