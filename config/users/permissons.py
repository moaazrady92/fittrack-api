from rest_framework.permissions import BasePermission ,SAFE_METHODS

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role.is_coach())

class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role.is_trainee())

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: #lets anyone read only but only user can edit it
            return True
        return obj == request.user #lets anyone see  unlike obj.user which only lets user access the page

class IsCoachOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role.is_coach()