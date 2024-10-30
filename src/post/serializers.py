from rest_framework import serializers
from user.serializers import UserSerializer
from post.domains import PostDomain

class PostSerializer(serializers.Serializer):
    content_url = serializers.URLField()

    def create(self, validated_data):
        return PostDomain(**validated_data)

    def to_representation(self, instance):
        # Handle the PostDomain to dictionary conversion here
        if isinstance(instance, PostDomain):
            return {
                'id': instance.id,
                'content_url': instance.content_url,
                'author': UserSerializer(instance.author).data,
                'likes_count': instance.likes_count,
            }
        return super().to_representation(instance)
