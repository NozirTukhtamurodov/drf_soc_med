# post/domains.py

from dataclasses import dataclass
from user.domains import UserDomain
from core.models import Post

@dataclass
class PostDomain:
    id: int
    content_url: str
    author: UserDomain
    likes_count: int = 0

    @staticmethod
    def to_domain(post: Post) -> "PostDomain":
        """Converts Django Post model to PostDomain"""
        return PostDomain(
            id=post.id,
            content_url=post.content_url,
            author=UserDomain.to_domain(post.author),
            likes_count=post.likes_count
        )

    def from_domain(self) -> Post:
        """Converts PostDomain to Django Post model"""
        post_obj = Post.objects.get(id=self.id) if self.id else Post()
        post_obj.content_url = self.content_url
        post_obj.author_id = self.author.id
        post_obj.likes_count = self.likes_count
        return post_obj

    def add_like(self):
        self.likes_count += 1
