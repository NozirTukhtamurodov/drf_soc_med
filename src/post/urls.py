from django.urls import path
from post.views import (
    CreatePostView, 
    MyPostsView, 
    LikedPostsView, 
    LikePostView, 
    UpdatePostView, 
    DeletePostView
)

urlpatterns = [
    path('', CreatePostView.as_view(), name='create_post'),  # POST request to create a post
    path('mine/', MyPostsView.as_view(), name='my_posts'),  # GET request to get user posts
    path('liked/', LikedPostsView.as_view(), name='liked_posts'),  # GET request to get liked posts
    path('<int:pk>/like/', LikePostView.as_view(), name='like_post'),  # POST request to like a post
    path('<int:pk>/', UpdatePostView.as_view(), name='update_post'),  # PATCH request to update a post
    path('<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),  # DELETE request to delete a post
]
