from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Category, Product

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        related_products = Product.objects.filter(category=category).exclude(slug=self.kwargs['slug'])[:3]
        context['related_products'] = related_products
        return context

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
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)[:3]
        context['related_products'] = related_products
        
        # Add product_id to context
        context['product_id'] = product.id
        
        return context

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset=queryset)
        except Product.DoesNotExist:
            return None