from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from src.posts.consumers import PostConsumer
from src.posts.views import PostViewset

router = SimpleRouter()


router.register("posts", PostViewset)

urlpatterns = []

urlpatterns += router.urls


websocket_urlpatterns = [
    path("ws/posts/<int:post_id>/", PostConsumer.as_asgi()),
]
