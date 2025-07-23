from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class book(models.Model):
    book_no=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=40)
    author=models.CharField(max_length=40)
    ctgry=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(upload_to='books',null=True,blank=True)
    def __str__(self):
        return self.name