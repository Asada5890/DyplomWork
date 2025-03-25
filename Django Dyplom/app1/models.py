from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
    


class User(models.Model):
    name = models.CharField(max_length=255)
    sur_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.IntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name