from django.urls import path
from . import views

urlpatterns = [
    path('<community>/all', views.RetrievePostList.as_view(), name="retrieve-post-list"),
    path('<slug>', views.RetrievePost.as_view(), name="retrieve-post"),
    path('<slug>/update', views.UpdatePost.as_view(), name="update-post"),
    path('<community>/create/normal', views.CreatePost.as_view(), name="create-post"),
    path('<slug>/delete', views.DeletePost.as_view(), name="delete-post"),
]
