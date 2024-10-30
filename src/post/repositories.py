from core.models import Post, User
from typing import List
from post.domains import PostDomain
from django.core.exceptions import ObjectDoesNotExist


class IPostRepository:
    def get_post_by_id(self, post_id: int) -> PostDomain | None:
        raise NotImplementedError

    def save_post(self, post: PostDomain) -> PostDomain:
        raise NotImplementedError

    def get_posts_by_user(self, user_id: int) -> list[PostDomain]:
        raise NotImplementedError

    def get_liked_posts_by_user(self, user) -> list[PostDomain]:
        raise NotImplementedError

    def delete_post(self, post: PostDomain):
        raise NotImplementedError

    def user_has_liked_post(self, user: User, post_id: int) -> bool:
        """Check if the user has already liked a post."""
        raise NotImplementedError


class PostRepository(IPostRepository):
    def __init__(self):
        pass

    def get_post_by_id(self, post_id: int) -> PostDomain:
        try:
            post = Post.objects.get(id=post_id)
            return PostDomain.to_domain(post)
        except ObjectDoesNotExist:
            return None

    def get_posts_by_user(self, user_id: int) -> List[PostDomain]:
        posts = Post.objects.filter(author_id=user_id)
        return [PostDomain.to_domain(post) for post in posts]

    def get_liked_posts_by_user(self, user) -> List[PostDomain]:
        posts = user.liked_posts.all()
        return [PostDomain.to_domain(post) for post in posts]

    def save_post(self, post: PostDomain) -> PostDomain:
        post_obj = post.from_domain()
        post_obj.save()
        return PostDomain.to_domain(post_obj)

    def delete_post(self, post: PostDomain):
        post_obj = post.from_domain()
        post_obj.delete()

    def user_has_liked_post(self, user: User, post_id: int) -> bool:
        """
        Check if the user has already liked the post.
        """
        return user.liked_posts.filter(id=post_id).exists()
