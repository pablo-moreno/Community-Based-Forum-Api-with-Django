from django.urls import path
from . import views as comments_views

urlpatterns = [
    path('', comments_views.ListCreateCommentAPIView.as_view(), name="comments-create-list"),
    path('<id>', comments_views.RetrieveUpdateDestroyCommentAPIView.as_view(), name="comments-retrieve-update-destroy"),
    path('<id>/<parent_id>/child', comments_views.GetChildCommentsAPIView.as_view(), name="comments-retrieve-child"),
]
