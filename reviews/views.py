from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review
from stock.models import Product
from orders.models import Order

class ReviewDetailView(View):
    """View for review detail."""
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        product = get_object_or_404(Product, id=kwargs['pk'])
        # get review
        review = get_object_or_404(
            Review,
            order=order,
            product=product,
        )
        context = {
            'product': product,
            'review': review,
        }
        return render(request, 'reviews/review_detail.html', context)

class CreateReviewView(LoginRequiredMixin, View):
    """View for creating a review."""
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        order = get_object_or_404(Order, id=self.kwargs['order_id'])
        user = request.user
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not (rating and comment):  # Handle missing fields
            return JsonResponse({'error': 'Rating and comment are required.'}, status=400)

        # Check if the user has already reviewed this product
        if Review.objects.filter(user=user, product=product, order=order).exists():
            return JsonResponse({'error': 'You have already reviewed this product.'}, status=400)
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                order=order,
                rating=rating,
                comment=comment
            )
            return JsonResponse({'success': True, 'review_id': review.id})

class DeleteReviewView(LoginRequiredMixin, View):
    """View for deleting a review."""
    def post(self, request, *args, **kwargs):
        review_id = kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        
        # Check if the user is the owner of the review
        if review.user == request.user:
            review.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'You do not have permission to delete this review.'}, status=403)
