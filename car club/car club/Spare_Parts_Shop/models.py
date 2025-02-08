from django.db import models
from Admin.models import *

# Create your models here.

class shop_tb(models.Model):
    logo=models.FileField(max_length=50)
    shop_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    district_id=models.ForeignKey('Admin.district_tb',on_delete=models.CASCADE,default='1')
    place=models.CharField(max_length=20)
    proof=models.FileField(max_length=50,default='none')
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    status=models.CharField(max_length=20,default='pending')

class spare_part_tb(models.Model):
    path=models.FileField(max_length=50)
    vehicle_id=models.ForeignKey('Admin.vehicle_tb',on_delete=models.CASCADE)
    brand_id=models.ForeignKey('Admin.brand_tb',on_delete=models.CASCADE)
    category_id=models.ForeignKey('Admin.part_category_tb',on_delete=models.CASCADE,default='1')
    part_name=models.CharField(max_length=20)
    details=models.CharField(max_length=100)
    price=models.CharField(max_length=20)
    stock=models.CharField(max_length=20)
    shop_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE,default='1')

class tracking_details_tb(models.Model):
    tracking_details=models.CharField(max_length=200)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20,default='0')
    order_id=models.ForeignKey('User.order_tb',on_delete=models.CASCADE)

class part_model_tb(models.Model):
    part_id=models.ForeignKey(spare_part_tb,on_delete=models.CASCADE)
    model_id=models.ForeignKey('Admin.model_tb',on_delete=models.CASCADE)
    
    
