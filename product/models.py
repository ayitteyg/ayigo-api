from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils.text import slugify

""" 

CLEANING MODELS/RESETTING DATABASE
.clean/delete all migration files excepts init.py
.rm -rf db.sqlite3 #this delete the database
.python manage.py makemigrations 
.python manage.py migrate
.python manage.py createsuperuser

"""




class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    desc = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.name)}-{str(self.uuid)[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (by {self.created_by.username})"