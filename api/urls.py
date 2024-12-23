from django.urls import path
from .views import PostListView, PostCreateView, PostEditView, PostDetailView

app_name='api'
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post_create/', PostCreateView.as_view(), name='create_post'),
    path('post_edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail')
]