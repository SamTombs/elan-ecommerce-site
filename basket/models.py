from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Basket(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Basket for {self.user.first_name} {self.user.last_name}"
    
    @property
    def total_items(self):

        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class BasketItem(models.Model):

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['basket', 'product']  # Prevent duplicate products in same basket
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.basket.user.email}'s basket"
    
    @property
    def total_price(self):
 
        return self.quantity * self.product.price
    
    def save(self, *args, **kwargs):

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        super().save(*args, **kwargs)
