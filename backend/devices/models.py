from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=50)
    max_clients = models.IntegerField()
    max_capacity = models.IntegerField()
    created_by = models.ForeignKey(User, related_name="devices", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)