from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, TaskSerializer
from .models import Task


# ===========================
# SIGNUP VIEW (PUBLIC)
# ===========================
@method_decorator(csrf_exempt, name="dispatch")
class SignupView(APIView):
    permission_classes = []  # Public route

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)

        return Response(serializer.errors, status=400)


# ===========================
# LOGIN VIEW (PUBLIC)
# ===========================
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = []  # Public route

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=200)


# ===========================
# TASK LIST + CREATE
# ===========================
class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ===========================
# TASK DETAIL (GET, UPDATE, DELETE)
# ===========================
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
