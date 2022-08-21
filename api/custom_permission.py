from rest_framework import permissions


class ProfileOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ChangePasswordPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id