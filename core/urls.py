from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.posts.urls")),
    path("", include("src.users.urls")),
    path("auth/", include("djoser.urls")),
]
