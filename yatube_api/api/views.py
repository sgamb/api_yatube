from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Comment, Group, Post

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя изменять чужой пост')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалять чужой пост')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя изменять чужой комментарий')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалять чужой комментарий')
        instance.delete()
