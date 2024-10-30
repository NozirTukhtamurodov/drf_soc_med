
from dataclasses import dataclass
from typing import Optional
from core.models import User

@dataclass
class UserDomain:
    id: int
    username: str
    avatar_url: Optional[str] = None

    @staticmethod
    def to_domain(user: User) -> "UserDomain":
        return UserDomain(
            id=user.id,
            username=user.username,
            avatar_url=user.avatar
        )

    def from_domain(self) -> User:
        user_obj = User.objects.get(id=self.id)
        user_obj.username = self.name
        user_obj.avatar = self.avatar_url
        return user_obj
    