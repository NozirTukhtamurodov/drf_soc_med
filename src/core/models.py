from django.db import models
from django.contrib.auth.models import AbstractUser


class NotificationType(models.TextChoices):
    like = "like", "Like"
    dislike = "dislike", "Dislike"


class User(AbstractUser):
    avatar = models.URLField(null=True, blank=True)
    liked_posts = models.ManyToManyField('Post', related_name='liked_by', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='User_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='User_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Post(models.Model):
    content_url = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=50, choices=NotificationType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
