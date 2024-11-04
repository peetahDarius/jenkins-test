from django.db import models

# Create your models here.

class Version(models.Model):
    custom_id = models.IntegerField(default=1)
    backend_version = models.CharField( max_length=50, default="1.0.0")
    frontend_version = models.CharField( max_length=50, default="1.0.0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)