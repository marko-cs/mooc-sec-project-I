"""
This module contains the configuration for the FlawsApp Django application.
"""

from django.apps import AppConfig

class FlawsappConfig(AppConfig):
    """
    Trival config such as app name
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "flawsapp"
