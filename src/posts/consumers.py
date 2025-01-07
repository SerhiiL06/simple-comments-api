import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from src.posts.models import Comment, Post


class PostConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def verify_token(self, token_dict):
        try:
            token = Token.objects.get(key=token_dict["token"])
        except Token.DoesNotExist:
            return False
        else:
            if token.user.is_active:
                return True
            else:
                return False

    @database_sync_to_async
    def save_comment(self, post_id, data: dict):
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.create(post=post, **data)

    async def connect(self):
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.group_name = f"post_{self.post_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        token = data.get("token")
        valid_token = await self.verify_token(json.loads(token))
        if not valid_token:
            await self.close()

        author = Token.objects.get(key=token).user

        data_to_save = {
            "author": author,
            "text": data.get("text"),
            "image": bytes_data.get("image"),
            "file": bytes_data.get("file"),
            "comment_patent_id": data.get("comment_parent_id"),
        }

        if bytes_data:
            content_file = ContentFile(bytes_data)
            if "image" in data:
                data_to_save["image"] = content_file
            else:
                data_to_save["file"] = content_file

        new_comment = await self.save_comment(self.post_id, data_to_save)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "new_comment",
                "message": {
                    "author": {
                        "id": new_comment.author.id,
                        "username": new_comment.author.username,
                        "email": new_comment.author.email,
                    },
                    "text": new_comment.text,
                    "comment_parent_id": new_comment.comment_parent_id,
                    "image": new_comment.image.url if new_comment.image else None,
                    "file": new_comment.file.url if new_comment.file else None,
                },
            },
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
