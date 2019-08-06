from django.urls import path
from . import views

urlpatterns = [
    path('<community>', views.ListCreatePostsAPIView.as_view(), name="posts-list-retrieve"),
    path('<id>', views.RetrieveUpdateDestroyPostAPIView.as_view(), name="posts-retrieve-update-destroy"),
]
