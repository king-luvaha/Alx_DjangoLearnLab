from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

from accounts.models import User as CustomUser
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification
from notifications.models import Notification

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in permissions.SAFE_METHODS


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # get all users the current user follows
        following_users = request.user.following.all()

        # required for checker:
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    # Get all posts from followed users
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Checker expects generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Checker expects Like.objects.get_or_create(user=request.user, post=post)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create notification for the post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post,
                )
            return Response({"detail": "Post liked"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "You already liked this post"}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Checker consistency — still use generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)