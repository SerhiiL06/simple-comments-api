from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django_resized import ResizedImageField
from mptt.models import MPTTModel, TreeForeignKey
from redis import Redis

from core.settings import AVAILABLE_FILE_EXT, AVAILABLE_IMAGE_EXT


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(max_length=1000)
    image = ResizedImageField(
        upload_to="post_images/",
        null=True,
        validators=[FileExtensionValidator(AVAILABLE_IMAGE_EXT)],
        size=[320, 240],
    )
    file = models.FileField(
        upload_to="post_files/",
        null=True,
        validators=[FileExtensionValidator(AVAILABLE_FILE_EXT)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]


class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    text = models.TextField(max_length=1000)
    image = ResizedImageField(
        upload_to="comment_images/",
        null=True,
        validators=[FileExtensionValidator(AVAILABLE_IMAGE_EXT)],
        size=[320, 240],
    )
    file = models.FileField(
        upload_to="comment_files/",
        null=True,
        validators=[FileExtensionValidator(AVAILABLE_FILE_EXT)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    comment_parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments_child",
    )

    class MPTTMeta:
        db_table = "comments"
        ordering = ["-created_at"]
        parent_attr = "comment_parent"
        order_insertion_by = ["-created_at"]
