from django.shortcuts import render
# recipes/views.py
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_user_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

class AuthenticatedGraphQLView(GraphQLView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        # Enforce authentication
        for auth_class in self.authentication_classes:
            auth = auth_class()
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
                break
        else:
            return JsonResponse({"message": "Invalid auth Token."})
        
        # Enforce permission checks
        for permission_class in self.permission_classes:
            permission = permission_class()
            if not permission.has_permission(request, self):

                return JsonResponse({"message": "You do not have permission to access this resource."})
        
        return super().dispatch(request, *args, **kwargs)