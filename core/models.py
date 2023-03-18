from django.db import models
from datetime import datetime

# Create your models here.
class Posts(models.Model):
    serial_no = models.CharField(max_length=30)
    image = models.ImageField(upload_to='licence_images')
    licence_number = models.CharField(max_length=30)
    date_recognized = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.date_recognized)

class MyImage(models.Model):
    serial_no = models.CharField(max_length=30)
    car_no = models.CharField(max_length=30)
    image = models.ImageField(upload_to='licence_images')
    def __str__(self):
        return str(self.car_no)