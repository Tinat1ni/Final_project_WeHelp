from django.urls import path
from .views import CharityView

app_name='charityGeorgia'

urlpatterns = [
    path('', CharityView.as_view(), name='charity' )
]