from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request.data.pop('token', None)  # Remove token if it exists
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # request.data.pop('token', None)  # Remove token if it exists
        request.META.pop('HTTP_AUTHORIZATION', None)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                token, _ = Token.objects.get_or_create(user=user)  # Get or create a token for the user
                return Response({'token': token.key}, status=status.HTTP_200_OK)  # Return the token
            return Response({'error': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Retrieve and delete the token associated with the user
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)
