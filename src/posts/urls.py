from rest_framework.routers import SimpleRouter
from src.posts.views import PostViewset

router = SimpleRouter()


router.register("posts", PostViewset)

urlpatterns = []

urlpatterns += router.urls
