from django.db import models
from Spare_Parts_Shop.models import *
from Workshop.models import *

# Create your models here.

class user_tb(models.Model):
    path=models.FileField(max_length=50)
    name=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    dob=models.CharField(max_length=20)
    district_id=models.ForeignKey('Admin.district_tb',on_delete=models.CASCADE,default='1')
    place=models.CharField(max_length=20)
    phone=models.CharField(max_length=20,default='phone')
    email=models.CharField(max_length=20,default='email')
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class cart_tb(models.Model):
    part_id=models.ForeignKey(spare_part_tb,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    count=models.IntegerField()
    total_price=models.CharField(max_length=20)
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    shop_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE,default='1')

class order_tb(models.Model):
    part_id=models.ForeignKey(spare_part_tb,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    count=models.IntegerField()
    total_price=models.CharField(max_length=20)
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    date=models.CharField(max_length=20,default='empty')
    time=models.CharField(max_length=20,default='empty')
    status=models.CharField(max_length=20,default='pending')
    shop_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE,default='1')
    prebook_id=models.CharField(max_length=10,null=True)

class bank_tb(models.Model):
    name=models.CharField(max_length=20,default='nil')
    credit_card_number=models.CharField(max_length=20)
    cvv=models.CharField(max_length=20)
    balance=models.CharField(max_length=20)

class payment_tb(models.Model):
    order_id=models.ForeignKey(order_tb,on_delete=models.CASCADE)
    amount=models.CharField(max_length=20)
    transaction_key=models.CharField(max_length=20)
    date=models.CharField(max_length=20,default='no date')
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE,default='1')
    shop_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE,default='1')
    status=models.CharField(max_length=20,default='pending')

class rating_tb(models.Model):
    part_id=models.ForeignKey(spare_part_tb,on_delete=models.CASCADE)
    rating=models.CharField(max_length=20)
    review=models.CharField(max_length=200)
    user_id=models.ForeignKey(user_tb,models.CASCADE)
    date=models.CharField(max_length=20,default='no date')

class complaint_tb(models.Model):
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    complaint=models.CharField(max_length=500)
    date=models.CharField(max_length=20)

class workshop_review_tb(models.Model):
    shop_id=models.ForeignKey(workshop_tb,on_delete=models.CASCADE)
    rating=models.CharField(max_length=20)
    review=models.CharField(max_length=500)
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    date=models.CharField(max_length=20,default='no date')

class prebook_tb(models.Model):
    part_id=models.ForeignKey(spare_part_tb,on_delete=models.CASCADE)
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    shop_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE)
    count=models.CharField(max_length=20,default='0')
    date=models.CharField(max_length=20,default='no date')
    time=models.CharField(max_length=20,default='no time')
    status=models.CharField(max_length=20,default='pending')

class notification_tb(models.Model):
    user_id=models.ForeignKey(user_tb,on_delete=models.CASCADE)
    seller_id=models.ForeignKey(shop_tb,on_delete=models.CASCADE)
    table=models.CharField(max_length=20)
    order_id=models.ForeignKey(order_tb,on_delete=models.CASCADE,null=True)
    prebook_id=models.ForeignKey(prebook_tb,on_delete=models.CASCADE,null=True)
    time=models.CharField(max_length=20,default='no time')
    date=models.CharField(max_length=20,default='no time')
    status=models.CharField(max_length=20,default='unread')
    
    
    
