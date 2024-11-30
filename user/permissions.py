
from rest_framework import permissions

''' For User '''
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class IsEventPlannerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'EVENT_PLANNER'

class IsVendorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'VENDOR'

class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'CLIENT'

''' For Events'''
class IsAdminOrEventPlannerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role in ['ADMIN', 'EVENT_PLANNER']:
            return True
        else:
            return False

class IsAdminOrVendorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role in ['ADMIN', 'VENDOR']:
            return True
        else:
            return False

class IsAdminOrClientOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role in ['ADMIN', 'CLIENT']:
            return True
        else:
            return False