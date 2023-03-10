

from rest_framework import permissions
import jwt

    
class IsAuthUser(permissions.BasePermission):

    def has_permission(self, request, view):
        token= request.headers['Authorization']

        try:
            jwt.decode(token, 'secret', algorithms=["HS256"])

        except jwt.exceptions.DecodeError:
            return False
        except jwt.exceptions.ExpiredSignatureError:
            return False
        
        return True
    
    



# class IsAuthOrRead(permissions.BasePermission):
    
#     def has_permission(self, request, view):

#         if request.user.is_authenticated:
#             return True
#         return False
    
#     def has_object_permission(self, request, view, obj):
        
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return obj.author == request.user