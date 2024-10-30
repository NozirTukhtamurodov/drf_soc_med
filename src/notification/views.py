from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from notification.services import get_service


class NotificationBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_service()


class NotificationView(NotificationBaseView):
    def get(self, request):
        notifications = self.service.get_user_notifications(user=request.user)
        return notifications.to_response()
