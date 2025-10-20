from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Basket(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class BasketItem(models.Model):

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def save(self, *args, **kwargs):

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        super().save(*args, **kwargs)
    