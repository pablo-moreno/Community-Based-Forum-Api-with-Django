from django.urls import path
from . import views as community_views

urlpatterns = [
    path('create', community_views.CreateCommunity.as_view(), name="create-community"),
    path('<slug>/destroy', community_views.DestroyCommunity.as_view(), name="destroy-community"),
    path('administrator', community_views.RetrieveCommunitiesAdministratedByUser.as_view(),
         name="get-communities-administrated-by-user"),
    path('moderator', community_views.RetrieveCommunitiesModeratedByUser.as_view(),
         name="get-communities-moderated-by-user"),
    path('<slug>/admin-update', community_views.UpdateCommunity.as_view(), name="admin-update-community"),
    path('<slug>/moderator-update', community_views.ModeratorUpdateCommunity.as_view(),
         name="moderator-update-community"),
    path('<slug>', community_views.RetrieveCommunity.as_view(), name="retrieve-community"),
]
