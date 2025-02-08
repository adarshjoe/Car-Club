from django.db import models
from User.models import *

# Create your models here.

class admin_tb(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class vehicle_tb(models.Model):
    vehicle_name=models.CharField(max_length=20)

class part_category_tb(models.Model):
    vehicle_id=models.ForeignKey(vehicle_tb,on_delete=models.CASCADE)
    category=models.CharField(max_length=30)

class brand_tb(models.Model):
    vehicle_id=models.ForeignKey(vehicle_tb,on_delete=models.CASCADE)
    brand_name=models.CharField(max_length=20)

class model_tb(models.Model):
    vehicle_id=models.ForeignKey(vehicle_tb,on_delete=models.CASCADE)
    brand_id=models.ForeignKey(brand_tb,on_delete=models.CASCADE)
    model_name=models.CharField(max_length=20)

class district_tb(models.Model):
    district_name=models.CharField(max_length=30)

class reply_tb(models.Model):
    complaint_id=models.ForeignKey(complaint_tb,on_delete=models.CASCADE)
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE,default=1)
    subject=models.CharField(max_length=100)
    reply=models.CharField(max_length=500)
    date=models.CharField(max_length=20)
    status=models.CharField(max_length=20,default='unread')
