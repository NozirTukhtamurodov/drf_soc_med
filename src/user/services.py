from user.repositories import UserRepository
from core.models import User
from user.serializers import UserSerializer
from rest_framework import status
from core.response import ServiceResponse
from abc import abstractmethod, ABC


class IUserService(ABC):
    @abstractmethod
    def get_user_profile(self, user: User) -> ServiceResponse:
        pass

    def update_user_profile(self, user: User, data: dict) -> ServiceResponse:
        pass


class UserService:
    def __init__(self, repository: UserRepository, serializer: UserSerializer):
        self.repository = repository
        self.serializer = serializer

    def get_user_profile(self, user: User) -> ServiceResponse:
        """
        Get the user profile, serialized for response.
        """
        serialized_user = self.serializer(user).data
        return ServiceResponse(data=serialized_user, status=status.HTTP_200_OK)

    def update_user_profile(self, user: User, data: dict) -> ServiceResponse:
        """
        Update the user's profile and return the updated data.
        """
        updated_user = self.repository.update_user(user, data)
        serialized_user = self.serializer(updated_user).data
        return ServiceResponse(data=serialized_user, status=status.HTTP_200_OK)


def get_service(serializer=UserSerializer) -> IUserService:
    return UserService(repository=UserRepository(), serializer=serializer)
