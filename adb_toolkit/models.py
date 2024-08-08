from django.db import models

# Create your models here.
from django.db import models


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.device_id
