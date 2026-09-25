from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsAdmin, IsManager


class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    GET:
        All authenticated users can view departments.

    POST:
        Only Admin and Manager can create departments.
    """

    queryset = Department.objects.select_related("manager").all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET:
        All authenticated users can view a department.

    PUT/PATCH:
        Admin and Manager can update.

    DELETE:
        Admin only.
    """

    queryset = Department.objects.select_related("manager").all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsManager()]

        return [IsAuthenticated()]