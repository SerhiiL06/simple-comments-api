from rest_framework import serializers
from src.posts.models import Post
from django.core.exceptions import ValidationError


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
    class Meta:
        model = Post
        fields = "__all__"
