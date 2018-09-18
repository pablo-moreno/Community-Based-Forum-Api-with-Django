from django.urls import path
from . import views as comments_views

urlpatterns = [
    path('<slug>/create', comments_views.CreateComment.as_view(), name="create-comment"),
    path('<slug>', comments_views.RetrieveCommentsByPost.as_view(), name="retrieve-comment-by-post"),
    path('delete/<id>', comments_views.DeleteCommentSerializer.as_view(), name="delete-comment"),
    path('update/<id>', comments_views.UpdateCommentSerializer.as_view(), name="update-comment"),
    path('<slug>/<parent_id>/child', comments_views.GetChildComments.as_view(), name="retrieve-child-comment"),
]
