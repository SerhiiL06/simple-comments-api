from __future__ import annotations

from django.core.exceptions import ValidationError
from rest_framework import serializers, status

from src.posts.models import Comment, Post
from src.users.serializers import ShortUserSerializer
from django.shortcuts import get_object_or_404


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["text", "image", "file"]

    def validate(self, attrs):
        request = self.context.get("request")
        if not hasattr(request, "user"):
            raise ValidationError("user instance is empty")
        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(many=False)

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(many=False)
    comments_child = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "text",
            "image",
            "file",
            "created_at",
            "comments_child",
        ]

    def get_comments_child(self, obj):
        child_comments = obj.comments_child.order_by("created_at")
        return CommentSerializer(child_comments, many=True).data


class DetailPostSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(many=False)
    post_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["author", "text", "image", "file", "created_at", "post_comments"]

    def get_post_comments(self, obj):
        root_comments = obj.post_comments.filter(level=0).order_by("created_at")
        return CommentSerializer(root_comments, many=True).data


class AddCommentSerializer(serializers.ModelSerializer):

    comment_parent_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ["text", "image", "file", "comment_parent_id"]

    def validate(self, attrs):
        context = self.context
        post_id = context.get("post_id")
        if not post_id:
            raise ValidationError(
                "post_id must be provided", status.HTTP_400_BAD_REQUEST
            )

        get_object_or_404(Post, pk=post_id)

        comment_parent = attrs.get("comment_parent_id")

        if comment_parent:
            comments_ids = Comment.objects.filter(post_id=post_id).values_list(
                "id", flat=True
            )

            if comment_parent not in comments_ids:
                raise ValidationError(
                    "Parent comment is not relevant to this post or the comment does not exist"
                )

        return super().validate(attrs)

    def create(self, validated_data):
        context = self.context
        validated_data["author"] = context.get("author")
        validated_data["post_id"] = context.get("post_id")
        return Comment.objects.create(**validated_data)
