from rest_framework import serializers
from notification.domains import NotificationDomain
from user.serializers import UserSerializer
from post.serializers import PostSerializer


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    post = PostSerializer()
    type = serializers.CharField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        if isinstance(instance, NotificationDomain):
            return {
                'id': instance.id,
                'user': UserSerializer(instance.user).data,
                'post': PostSerializer(instance.post).data,
                'type': instance.type,
                'created_at': instance.created_at,
            }
        return super().to_representation(instance)
