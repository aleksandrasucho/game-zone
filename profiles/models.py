from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import date

class Profile(models.Model):
    """Model for the profiles."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User',
        help_text=(
            'format: required, unique=True'
        )
    )
    
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='First name',
        help_text=(
            'format: not required, max_length=50'
        )
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Last name',
        help_text=(
            'format: not required, max_length=50'
        )
    )
    
    avatar = CloudinaryField(
        'avatar',
        folder='avatars',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
    )
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        return self.user.username
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default_avatar.svg'
    
class Address(models.Model):
    """Model for the addresses."""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='Profile',
        help_text=(
            'format: required'
        )
    )
    address_line = models.CharField(
        max_length=100,
        verbose_name='Address line',
        help_text=(
            'format: required, max_length=100'
        )
    )
    city = models.CharField(
        max_length=50,
        verbose_name='City',
        help_text=(
            'format: required, max_length=50'
        )
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Country',
        help_text=(
            'format: required, max_length=50'
        )
    )
    county_region = models.CharField(
        max_length=50,
        verbose_name='County/Region',
        help_text=(
            'format: required, max_length=50'
        )
    )
    zip_code = models.CharField(
        max_length=20,
        verbose_name='Zip code',
        help_text=(
            'format: required, max_length=20'
        )
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Primary',
        help_text=(
            'format: not required'
        )
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Phone number',
        help_text=(
            'format: required, max_length=20'
        )
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
    )

    def __str__(self):
        """Return the address line."""
        return f'{self.profile.user.username} - {self.zip_code} - {self.is_primary}'

    def save(self, *args, **kwargs):
        """Check if there is a primary address."""
        super().save(*args, **kwargs)
        if self.is_primary:
            for address in self.profile.addresses.all().exclude(id=self.id):
                address.is_primary = False
                address.save()