from rest_framework import serializers
from src.posts.models import Post


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["text", "image", "file"]
