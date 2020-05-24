from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return True

        # if user.is_authenticated and request.method in ['GET', 'PATCH', 'PUT', 'POST', 'DELETE']:
        #     user_companies = user.user_companies.all()
        #     if hasattr(obj, 'company'):
        #         return obj.company in user_companies
        #     if hasattr(obj, 'department'):
        #         return obj.department.company in user_companies
        #     if hasattr(obj, 'commission'):
        #         return obj.commission.company in user_companies
        #     if hasattr(obj, 'event'):
        #         return obj.event.company in user_companies
        #     return obj in user_companies

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated and request.method in ['GET', 'PATCH', 'PUT', 'POST', 'DELETE']:
            user_companies = user.user_companies.all()
            if hasattr(obj, 'company'):
                return obj.company in user_companies
            if hasattr(obj, 'department'):
                return obj.department.company in user_companies
            if hasattr(obj, 'workplace'):
                return obj.workplace.department.company in user_companies
            if hasattr(obj, 'commission'):
                return obj.commission.company in user_companies
            if hasattr(obj, 'event'):
                return obj.event.company in user_companies
            return obj in user_companies



class ByDirectionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        user_groups = user.groups.all()

        import pdb; pdb.set_trace()

        if user.is_authenticated:
            for group in user_groups:
                if group in [1,2,3]:
                    return True
                else:
                    continue
            if request.method in ['PATCH', 'PUT', 'POST', 'DELETE']:
                user_directions = user.directions.all()
                if hasattr(obj, 'direction'):
                    return obj.direction in user_directions
                if hasattr(obj, 'dev') and getattr(obj, 'dev', None) is not None:
                    return obj.dev.direction in user_directions
                if hasattr(obj, 'task') and getattr(obj, 'task', None) is not None:
                    return obj.task.dev.direction in user_directions
                return obj in user_directions
        else:
            return False
            