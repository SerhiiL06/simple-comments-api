from rest_framework import viewsets
from src.posts.models import Post
from src.posts.serializers import PostSerializer, CreatePostSerializer
from rest_framework import permissions


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePostSerializer
        return super().get_serializer_class()
