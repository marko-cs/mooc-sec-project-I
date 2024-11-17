"""
This module defines the database models for the flawsapp application.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class URLNotes(models.Model):
    """
    URLNotes model represents user-specific notes associated with URLs.
    Each entry is identified by a unique UUID.
    """

    # A01:2021 – Broken Access Control
    # on_delete=models.CASCADE should be added to ForeignKey definition below
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, auto_created=True
    )
    notes = models.TextField()
    url = models.URLField()
