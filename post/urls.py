from django.urls import path
from .views import PostCreateView,  PostListByCategoryView, PostListView, PostSearchView, PostDetailView

app_name='post'

urlpatterns = [
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('category/<str:category_name>/', PostListByCategoryView.as_view(), name='posts_by_category'),
    path('', PostListView.as_view(), name='post_list'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
]
