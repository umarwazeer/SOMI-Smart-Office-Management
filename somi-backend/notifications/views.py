from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = NotificationSerializer(
            data=data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=request.user,
            )
        except Notification.DoesNotExist:
            return Response(
                {
                    "detail": "Notification not found."
                },
                status=404,
            )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        serializer = NotificationSerializer(
            notification
        )

        return Response(serializer.data)
    
    
class NotificationUnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()

        return Response(
            {
                "unread_count": unread_count
            }
        )
        
      
class NotificationMarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True)

        return Response(
            {
                "message": "All notifications marked as read.",
                "updated_count": updated_count,
            }
        )      