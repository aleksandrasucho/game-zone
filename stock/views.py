from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Category, Product

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # Number of products per page

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')  # Retrieve category slug from URL parameter
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)  # Filter products by category slug
        
        # Sorting
        sort_option = self.request.GET.get('sort')
        if sort_option == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_option == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort_option == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Paginate queryset
        products = context['products']
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        
        # Add product_id to context
        context['product_id'] = self.kwargs.get('product_id')
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'stock/product_detail.html'  # Ensure this matches the path to your template
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Fetch related products (excluding the current product)
        related_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)[:3]
        context['related_products'] = related_products
        
        # Add product_id to context
        context['product_id'] = product.id
        
        return context

    def get_object(self, queryset=None):
        # Override get_object method to handle DoesNotExist exception
        try:
            return super().get_object(queryset=queryset)
        except Product.DoesNotExist:
            return None