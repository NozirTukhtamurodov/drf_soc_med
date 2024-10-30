from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from post.services import get_service
from drf_yasg.utils import swagger_auto_schema
from post.serializers import PostSerializer


class PostBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_service()


class CreatePostView(PostBaseView):
    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={201: PostSerializer}
    )
    def post(self, request):
        service_response = self.service.create_post(data=request.data, user=request.user)
        return service_response.to_response()


class MyPostsView(PostBaseView):
    def get(self, request):
        service_response = self.service.get_user_posts(user=request.user)
        return service_response.to_response()


class LikedPostsView(PostBaseView):
    def get(self, request):
        service_response = self.service.get_liked_posts(user=request.user)
        return service_response.to_response()


class LikePostView(PostBaseView):
    def post(self, request, pk):
        service_response = self.service.like_post(post_id=pk, user=request.user)
        return service_response.to_response()


class UpdatePostView(PostBaseView):
    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={200: PostSerializer}
    )
    def patch(self, request, pk):
        service_response = self.service.update_post(post_id=pk, data=request.data, user=request.user)
        return service_response.to_response()


class DeletePostView(PostBaseView):
    def delete(self, request, pk):
        service_response = self.service.delete_post(post_id=pk, user=request.user)
        return service_response.to_response()
