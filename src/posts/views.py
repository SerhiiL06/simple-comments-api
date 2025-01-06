from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.posts.models import Post
from src.posts.serializers import (
    AddCommentSerializer,
    CreatePostSerializer,
    DetailPostSerializer,
    PostSerializer,
)


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePostSerializer
        if self.action == "retrieve":
            return DetailPostSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "retrieve":
            return Post.objects.prefetch_related(
                "post_comments__comments_child"
            ).select_related("author")
        return super().get_queryset()

    @action(
        methods=["post"],
        detail=True,
        serializer_class=AddCommentSerializer,
        url_path="add-comment",
    )
    def add_comment(self, request, *args, **kwargs):

        post_instance = self.get_object()

        serializer = AddCommentSerializer(
            data=request.data,
            context={"post_id": post_instance.id, "author": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
