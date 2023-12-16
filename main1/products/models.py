from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    #title = models.CharField(max_length=255, )
    #image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class ProductUser(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    product_id = models.IntegerField(unique=True)


class User(models.Model):
    pass
    
