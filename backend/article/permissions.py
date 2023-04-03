from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    允许管理员进行修改，其他用户仅可查看
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_superuser
    