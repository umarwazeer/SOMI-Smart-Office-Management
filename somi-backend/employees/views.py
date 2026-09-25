from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsManager

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.select_related(
        "user",
        "department",
    ).all()

    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.select_related(
        "user",
        "department",
    ).all()

    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsManager()]

        return [IsAuthenticated()]