from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    book_no=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=40)
    author=models.CharField(max_length=40)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(upload_to='books',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name
    
    @property
    def is_available(self):
        return self.available_copies > 0
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile',blank=True,null=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    fullname=models.CharField(max_length=30,null=True,blank=True)
    address=models.TextField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.user.username
    
    
    
class Borrow(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    borrow_date=models.DateTimeField(default=timezone.now)
    return_date=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return f"{self.user.username} borrowed{self.book.name}"
    
    @property
    def is_returned(self):
        return self.return_date is not None