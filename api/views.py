from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from post.models import Post, Category
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class PostListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        custom_input_1 = self.request.data.get('custom_input_1', '')
        custom_input_2 = self.request.data.get('custom_input_2', '')

        if custom_input_1:
            post.custom_input_1 = custom_input_1
        if custom_input_2:
            post.custom_input_2 = custom_input_2

        if not self.request.FILES.get('picture'):
            post.picture = 'default_images/default_picture.png'

        post.save()

        return post


class PostEditView(UpdateAPIView):
    model = Post
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'], author=self.request.user)
        return post

    def perform_update(self, serializer):
        serializer.save()


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'