from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import os

schema_view = get_schema_view(
   openapi.Info(
      title="Social Network API",
      default_version='v1',
      description="API documentation for Social Network",
   ),
   url=os.getenv('API_HOST', ''),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls')),
    path('api/posts/', include('post.urls')),
    path('api/notifications/', include('notification.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
