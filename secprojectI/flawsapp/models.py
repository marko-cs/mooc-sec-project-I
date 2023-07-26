from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class URLNotes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created = True)
	notes = models.TextField()
	url = models.URLField()
