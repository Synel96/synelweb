from django.urls import path
from .views import ReviewListAPIView

urlpatterns = [
    path("list/",ReviewListAPIView.as_view(), name="review-list"),
]