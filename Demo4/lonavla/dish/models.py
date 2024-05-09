from django.db import models
from django.contrib.auth.models import *

class Dish(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL,null = True,blank = True)
    dish_name = models.CharField(max_length = 500)
    dish_description = models.TextField()
    dish_image = models.ImageField(upload_to='reciepe')
    dish_view_count = models.IntegerField(default = 1)
