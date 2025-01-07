from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from src.posts.models import Post
from src.posts.paginators import PostPaginator
from src.posts.serializers import (AddCommentSerializer, CreatePostSerializer,
                                   DetailPostSerializer, PostSerializer)


@extend_schema(tags=["posts"])
class PostViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPaginator
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["author__email", "author__username"]
    ordering_fields = ["author__email", "author__username", "created_at"]

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="comment_page",
                type=OpenApiTypes.INT,
                required=False,
                location=OpenApiParameter.QUERY,
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
