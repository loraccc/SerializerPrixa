from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify

# Create your models here.


class item(models.Model):
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generates the slug based on the 'name' field
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed

    def __str__(self):
        return self.user.username
