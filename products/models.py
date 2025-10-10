from itertools import product
from django.db import models

class Product(models.Model):
  def __str__(self):
    return f'{self.name} - {self.price}'
  name = models.CharField(max_length=60, unique=True)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  sizes = models.CharField(max_length=60)
  product_image = models.ImageField(upload_to='products/', height_field=None, width_field=None, max_length=100)