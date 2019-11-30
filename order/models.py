from django.db import models
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    
    order_number=models.CharField(max_length=200)
    customer_code=models.CharField(max_length=200)
    order_date=models.DateField('date ordered')
    assign_date=models.DateField('date assigned')
    survey_locations=models.CharField(max_length=200)
    depot_code=models.CharField(max_length=200)
    depot_name=models.CharField(max_length=200)
    unit_type=models.CharField(max_length=200)
    qty=models.IntegerField()
    release_number=models.CharField(max_length=200,default='0')
    survey_code=models.CharField(max_length=200)
    remark=models.TextField()

    def __str__(self):
        return self.order_number

class Container(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    container_number=models.CharField(max_length=200)
    content=models.TextField()

    def __str__(self):
        return self.container_number

class Customer(models.Model):
    customer_code=models.CharField(max_length=200)
    order_count=models.IntegerField()

    def __str__(self):
        return self.customer_code
