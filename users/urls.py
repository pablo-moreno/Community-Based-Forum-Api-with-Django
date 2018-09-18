from django.urls import path
from users import views as users_views

urlpatterns = [
    path('', users_views.UserProfile.as_view(), name="get-user-profile"),
    path('create', users_views.CreateUser.as_view(), name="create-user-profile"),
]
