from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.services import get_service
from user.serializers import UserSerializer


class UserBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.service = get_service()


class ProfileView(UserBaseView):
    @swagger_auto_schema(
        responses={200: UserSerializer}
    )
    def get(self, request):
        """
        Get the authenticated user's profile.
        """
        service_response = self.service.get_user_profile(user=request.user)
        return service_response.to_response()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, example="john_doe"),
                'avatar': openapi.Schema(type=openapi.TYPE_STRING, example="http://example.com/avatar.jpg"),
            }
        ),
        responses={200: UserSerializer}
    )
    def patch(self, request):
        """
        Partially update the user's name or avatar.
        Example:
        PATCH /profile/
        {
            "avatar": "http://example.com/new_avatar.jpg"
        }
        """
        service_response = self.service.update_user_profile(user=request.user, data=request.data)
        return service_response.to_response()
