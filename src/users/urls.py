from rest_framework.routers import SimpleRouter
from src.users.views import UserViewset

router = SimpleRouter()


router.register("register", UserViewset)

urlpatterns = []

urlpatterns += router.urls
