from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    industry = models.CharField(max_length=100)

    REQUIRED_FIELDS = ['email', 'full_name', 'contact_number', 'company_name', 'address', 'industry']

    def __str__(self):
        return self.username
