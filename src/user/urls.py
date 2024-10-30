from django.urls import path
from user.views import ProfileView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
]
