from django.urls import path
from .views import ReviewDetailView, CreateReviewView, DeleteReviewView

urlpatterns = [
    path('review/<int:order_id>/<int:product_id>/', ReviewDetailView.as_view(), name='review_detail'),
    path('review/<int:order_id>/<int:product_id>/add/', CreateReviewView.as_view(), name='create_review'),
    path('review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    # Other URL patterns if needed
]
