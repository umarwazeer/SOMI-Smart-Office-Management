from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin, IsManager, IsStaffMember
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserManagementSerializer,
)


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserManagementListCreateView(generics.ListCreateAPIView):
    """
    User Management endpoint.

    ADMIN:
        - View users
        - Create users

    MANAGER:
        - View users
        - Create users

    EMPLOYEE:
        - No access
    """

    serializer_class = UserManagementSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        queryset = User.objects.all().order_by(
            "-created_at"
        )

        search = self.request.query_params.get(
            "search"
        )

        role = self.request.query_params.get(
            "role"
        )

        status_filter = self.request.query_params.get(
            "status"
        )

        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )

        if role:
            queryset = queryset.filter(
                role=role.upper()
            )

        if status_filter:
            status_filter = status_filter.upper()

            if status_filter == "ACTIVE":
                queryset = queryset.filter(
                    is_active=True,
                    is_active_account=True
                )

            elif status_filter == "INACTIVE":
                queryset = queryset.filter(
                    is_active=False
                )

            elif status_filter == "DISABLED":
                queryset = queryset.filter(
                    is_active_account=False
                )

        return queryset


class UserManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    User Management detail endpoint.

    ADMIN:
        - View
        - Update
        - Delete

    MANAGER:
        - View
        - Update
        - Cannot delete
    """

    serializer_class = UserManagementSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return User.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.role != User.Role.ADMIN:
            return Response(
                {
                    "detail": (
                        "Only administrators can delete users."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()

        if instance.pk == request.user.pk:
            return Response(
                {
                    "detail": (
                        "You cannot delete your own account."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)

        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_200_OK
        )


class AdminOnlyTestView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "message": "Admin access granted.",
            "user": request.user.username,
            "role": request.user.role,
        })


class ManagerOnlyTestView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        return Response({
            "message": "Manager or Admin access granted.",
            "user": request.user.username,
            "role": request.user.role,
        })


class StaffTestView(APIView):
    permission_classes = [IsStaffMember]

    def get(self, request):
        return Response({
            "message": "Staff access granted.",
            "user": request.user.username,
            "role": request.user.role,
        })