from django.urls import path
from .views import HomeView, RegisterView,  VerificationView, ChoosePostView, ProfileView, PostEditView
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'user'
urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', VerificationView.as_view(), name='verify_code'),
    path('choose/<int:post_pk>/', ChoosePostView.as_view(), name='choose_post'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
]