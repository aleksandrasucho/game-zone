from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('profile/', include('profiles.urls')),
    path('orders/', include('orders.urls')), 
    path('newsletter/', include('newsletter.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('reviews/', include('reviews.urls')),
    path('stock/', include('stock.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
]
