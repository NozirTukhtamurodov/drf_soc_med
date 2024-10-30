from dataclasses import dataclass
from datetime import datetime
from user.domains import UserDomain
from post.domains import PostDomain


@dataclass
class NotificationDomain:
    id: int
    user: UserDomain
    post: PostDomain
    type: str
    created_at: datetime

    @staticmethod
    def to_domain(notification) -> "NotificationDomain":
        return NotificationDomain(
            id=notification.id,
            user=UserDomain.to_domain(notification.user),
            post=PostDomain.to_domain(notification.post),
            type=notification.notification_type,
            created_at=notification.created_at
        )

    def from_domain(self):
        """Convert domain to Notification model instance"""
        from core.models import Notification
        notification = Notification.objects.get(id=self.id) if self.id else Notification()
        notification.user_id = self.user.id
        notification.post_id = self.post.id
        notification.type = self.type
        return notification
