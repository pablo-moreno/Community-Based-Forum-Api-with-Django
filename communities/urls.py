from django.urls import path
from . import views as community_views

urlpatterns = [
    path('', community_views.ListCreateCommunity.as_view(), name="community-list-create"),
    path('<id>', community_views.UpdateRetrieveDestroyCommunityAPIView.as_view(),
         name="community-update-destroy-retrieve"),
]
