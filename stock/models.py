from django.db import models
from django.utils.text import slugify
from django.db import IntegrityError

class Category(models.Model):
    """Category model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category Name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category Slug',
        help_text='format: required, max_length=150'
    )
    is_active = models.BooleanField(
        default=False,
        choices=[(True, 'Active'), (False, 'Inactive')],
        verbose_name='Is Active'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    
    class Meta:
        """Meta class for Category model"""
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        """String representation of Category model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle IntegrityError, possibly due to duplicate slug
            pass

    @classmethod
    def get_active_categories(cls):
        """Get active categories"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_categories(cls):
        """Get not active categories"""
        return cls.objects.filter(is_active=False)

class Product(models.Model):
    """Product model"""
    name = models.CharField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Product Name',
        help_text='format: required, max_length=150'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Product Slug',
        help_text='format: required, max_length=150'
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Product Description',
        help_text='format: required'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Category',
        help_text='format: required'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        verbose_name='Price',
        help_text='format: required'
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Product Image'
    )

    class Meta:
        """Meta class for Product model"""
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        """String representation of Product model"""
        return self.name

    def save(self, *args, **kwargs):
        """Override save method to generate slug"""
        self.slug = slugify(self.name, allow_unicode=True)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle IntegrityError, possibly due to duplicate slug
            pass