from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
  def __str__(self):
    return f'{self.name} - {self.price}'
  name = models.CharField(max_length=60, unique=True)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  sizes = models.CharField(max_length=60)
  product_image = models.CharField(max_length=60)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)