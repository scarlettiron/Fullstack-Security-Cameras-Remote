from rest_framework import permissions

class is_household_member(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if self.request.user.household == obj.household or self.request.user.isAdmin:
            return True
        return False