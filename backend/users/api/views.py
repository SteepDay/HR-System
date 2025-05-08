from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Добавляем кастомные данные к ответу
        user = serializer.user
        response_data = {
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
            'email': user.email,
            'role': user.role,
            'user_id': user.id
        }
        
        return Response(response_data)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)