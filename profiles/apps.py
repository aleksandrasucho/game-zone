from django.apps import AppConfig
from django.db.models.signals import post_save


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        # Import signal handlers inside the ready method to avoid circular imports
        from .signals import create_profile, save_profile  # Import from the local package
        from django.contrib.auth.models import User
        
        # Connect signals to signal handlers
        post_save.connect(create_profile, sender=User)
        post_save.connect(save_profile, sender=User)