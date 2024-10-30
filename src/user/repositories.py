# user/repositories.py

from core.models import User

class UserRepository:
    def get_user_by_id(self, user_id: int) -> User:
        return User.objects.get(id=user_id)

    def update_user(self, user: User, data):
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user
