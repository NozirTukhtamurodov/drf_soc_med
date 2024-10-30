from post.repositories import PostRepository
from core.models import User
from post.domains import PostDomain
from rest_framework import status
from core.response import ServiceResponse
from post.serializers import PostSerializer
from notification.services import get_service as get_notification_service
from abc import ABC, abstractmethod


class IPostService(ABC):
    @abstractmethod
    def attach_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, post, user):
        pass

    @abstractmethod
    def create_post(self, data: dict, user: User) -> ServiceResponse:
        pass

    @abstractmethod
    def get_user_posts(self, user: User) -> ServiceResponse:
        pass

    @abstractmethod
    def like_post(self, post_id: int, user: User) -> ServiceResponse:
        pass

    @abstractmethod
    def update_post(self, post_id: int, data: dict, user: User) -> ServiceResponse:
        pass

    @abstractmethod
    def delete_post(self, post_id: int, user: User) -> ServiceResponse:
        pass

    @abstractmethod
    def get_liked_posts(self, user: User) -> ServiceResponse:
        pass


class PostService(IPostService):
    def __init__(self, repository: PostRepository, serializer_class=PostSerializer):
        """
        Initialize the PostService with repository and serializer.
        """
        self.repository = repository
        self.serializer_class = serializer_class
        self.observers = []

    def attach_observer(self, observer):
        """Attach an observer that listens to post changes."""
        self.observers.append(observer)

    def notify_observers(self, post, user):
        """Notify all observers when an event happens."""
        for observer in self.observers:
            observer.create_notification(post=post, liked_by_user=user)

    def create_post(self, data: dict, user: User) -> ServiceResponse:
        """
        Validate data using serializer
        """
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return ServiceResponse(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the post domain and save
        post_domain = PostDomain(id=None, content_url=serializer.validated_data['content_url'], author=user)
        saved_post = self.repository.save_post(post_domain)

        # Serialize the saved post domain
        serialized_post = self.serializer_class(saved_post).data
        return ServiceResponse(data=serialized_post, status=status.HTTP_201_CREATED)

    def get_user_posts(self, user: User) -> ServiceResponse:
        posts = self.repository.get_posts_by_user(user.id)
        serialized_posts = self.serializer_class(posts, many=True).data
        return ServiceResponse(data=serialized_posts, status=status.HTTP_200_OK)

    def get_liked_posts(self, user: User) -> ServiceResponse:
        posts = self.repository.get_liked_posts_by_user(user)
        serialized_posts = self.serializer_class(posts, many=True).data
        return ServiceResponse(data=serialized_posts, status=status.HTTP_200_OK)

    def like_post(self, post_id: int, user: User) -> ServiceResponse:
        post = self.repository.get_post_by_id(post_id)
        if not post:
            return ServiceResponse(message=f"Post with id {post_id} does not exist.", status=status.HTTP_404_NOT_FOUND)

        if self.repository.user_has_liked_post(user=user, post_id=post_id):
            return ServiceResponse(message="You have already liked this post.", status=status.HTTP_400_BAD_REQUEST)

        post.add_like()
        self.repository.save_post(post)
        model_post = post.from_domain()
        user.liked_posts.add(model_post)  # Add the Post model, not the domain object
        # Notify observers when a post is liked
        self.notify_observers(post=post, user=user)

        return ServiceResponse(data={'post_id': post_id, 'status': 'liked'}, status=status.HTTP_200_OK)

    def update_post(self, post_id: int, data: dict, user: User) -> ServiceResponse:
        # Validate data
        serializer = self.serializer_class(data=data, partial=True)
        if not serializer.is_valid():
            return ServiceResponse(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve post and check permissions
        post = self.repository.get_post_by_id(post_id)
        if not post:
            return ServiceResponse(message=f"Post with id {post_id} does not exist.", status=status.HTTP_404_NOT_FOUND)
        if post.author.id != user.id:
            return ServiceResponse(message="You are not authorized to edit this post", status=status.HTTP_403_FORBIDDEN)
        
        # Update post
        post.content_url = serializer.validated_data.get('content_url', post.content_url)
        self.repository.save_post(post)

        # Serialize updated post
        serialized_post = self.serializer_class(post).data
        return ServiceResponse(data=serialized_post, status=status.HTTP_200_OK)

    def delete_post(self, post_id: int, user: User) -> ServiceResponse:
        post = self.repository.get_post_by_id(post_id)
        if not post:
            return ServiceResponse(message=f"Post with id {post_id} does not exist.", status=status.HTTP_404_NOT_FOUND)

        if post.author.id != user.id:
            return ServiceResponse(message="You are not authorized to delete this post", status=status.HTTP_403_FORBIDDEN)

        self.repository.delete_post(post)
        return ServiceResponse(message="Post deleted successfully", status=status.HTTP_200_OK)


def get_service(serializer_class=PostSerializer) -> IPostService:
    """
    Create and return an instance of PostService with the provided serializer.
    If no serializer is passed, it defaults to PostSerializer.
    """
    post_service = PostService(repository=PostRepository(), serializer_class=serializer_class)
    notification_service = get_notification_service()
    post_service.attach_observer(notification_service)
    return post_service
