from rest_framework import permissions


class ProfileOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        # Instance must have an attribute named `user`.
        return obj.user == request.user


class ChangePasswordPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        # Instance must have an attribute named `user`.
        return obj.id == request.user.id