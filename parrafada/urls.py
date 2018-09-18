from django.contrib import admin
from django.urls import path, include

from debug_toolbar import urls as debug_urls

from users import urls as users_urls
from communities import urls as community_urls
from posts import urls as posts_urls
from comments import urls as comments_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
    path('community/', include(community_urls)),
    path('posts/', include(posts_urls)),
    path('comments/', include(comments_urls)),

    path('__debug__/', include(debug_urls))
]
