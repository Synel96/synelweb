from django.urls import path
from .views import ReviewCreateListAPIView

urlpatterns = [
    path("reviews/",ReviewCreateListAPIView.as_view(), name="review-list"),
]