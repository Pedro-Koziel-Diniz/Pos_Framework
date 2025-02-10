from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })

@api_view(['GET'])
def get_user_api_key(request):
    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})
    return Response({'error': 'Usuário não autenticado'}, status=401)
