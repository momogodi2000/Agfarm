from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, authenticate, login, logout
from .serializers import UserSerializer, RegisterSerializer
import random
from django.contrib.auth.hashers import check_password

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user_data = request.data
        try:
            serializer_class = RegisterSerializer(data=user_data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response({
                    "message": "User registered successfully !"
                }, status.HTTP_200_OK)  
            return Response({
                "message": "Error "+str(serializer_class.errors)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        try:
            if not check_password(password, user.password):
                return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)    

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        # Send OTP to user's phone number. Here, you need to integrate with an SMS service provider.
        user.otp = otp
        user.save()
        return Response({'message': 'OTP sent to your phone number.'})

    def put(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(phone_number=phone_number, otp=otp)
        except User.DoesNotExist:
            return Response({'error': 'Invalid OTP or phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.otp = None
        user.save()
        return Response({'message': 'Password has been reset successfully.'})
