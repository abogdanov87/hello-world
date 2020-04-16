from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated and request.method in ['GET', 'PATCH', 'PUT', 'POST', 'DELETE']:
            user_companies = user.user_companies.all()
            if hasattr(obj, 'company'):
                return obj.company in user_companies
            if hasattr(obj, 'department'):
                return obj.department.company in user_companies
            if hasattr(obj, 'commission'):
                return obj.commission.company in user_companies
            if hasattr(obj, 'event'):
                return obj.event.company in user_companies
            return obj in user_companies
            