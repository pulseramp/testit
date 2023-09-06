from django.db import models


# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
   is_registration_enabled = models.BooleanField(default=True)
