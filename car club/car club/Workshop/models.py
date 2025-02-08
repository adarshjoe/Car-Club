from django.db import models
from Admin.models import *
from User.models import *

# Create your models here.

class workshop_tb(models.Model):
    logo=models.FileField(max_length=50)
    shop_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    district_id=models.ForeignKey('Admin.district_tb',on_delete=models.CASCADE,default='1')
    place=models.CharField(max_length=20)
    proof=models.FileField(max_length=20,default='none')
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
    

class service_tb(models.Model):
    service_img=models.FileField(default='no pic')
    shop_id=models.ForeignKey(workshop_tb,on_delete=models.CASCADE)
    service=models.CharField(max_length=30)
    description=models.CharField(max_length=500)
    status=models.CharField(max_length=20)
