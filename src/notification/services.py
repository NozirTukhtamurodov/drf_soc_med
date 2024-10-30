from notification.repositories import INotificationRepository, NotificationRepository
from core.models import User, NotificationType
from notification.domains import NotificationDomain
from rest_framework import status
from core.response import ServiceResponse
from datetime import datetime
from notification.serializers import NotificationSerializer
from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    def get_user_notifications(self, user: User):
        pass    
    
    @abstractmethod
    def create_notification(self, post, liked_by_user):
        pass


class NotificationService(INotificationService):
    def __init__(self, repository: INotificationRepository, serializer: NotificationSerializer):
        self.repository = repository
        self.serializer = serializer

    def get_user_notifications(self, user: User):
        notifications = self.repository.get_notifications_for_user(user.id)
        serialized_notifications = self.serializer(notifications, many=True).data
        return ServiceResponse(data=serialized_notifications, status=status.HTTP_200_OK)

    def create_notification(self, post, liked_by_user):
        """
        Create a notification when a post is liked.
        """
        notification_domain = NotificationDomain(
            id=None,
            user=post.author,
            post=post,
            type=NotificationType.like.value,
            created_at=datetime.now()  # Corrected to use datetime object
        )
        saved_notification = self.repository.save_notification(notification_domain)
        return saved_notification


def get_service(serializer=NotificationSerializer) -> INotificationService:
    return NotificationService(repository=NotificationRepository(), serializer=serializer)
