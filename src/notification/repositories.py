from core.models import Notification
from notification.domains import NotificationDomain
from abc import ABC, abstractmethod


class INotificationRepository(ABC):
    @abstractmethod
    def get_notifications_for_user(self, user_id: int):
        pass

    @abstractmethod
    def save_notification(self, notification: NotificationDomain):
        pass


class NotificationRepository(INotificationRepository):
    def get_notifications_for_user(self, user_id: int):
        notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
        return [NotificationDomain.to_domain(notification) for notification in notifications]

    def save_notification(self, notification: NotificationDomain):
        notification_model = notification.from_domain()
        notification_model.save()
        return NotificationDomain.to_domain(notification_model)
