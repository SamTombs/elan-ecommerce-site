from django.db import models

class Review(models.Model):
    def __str__(self):
        return f'{self.text} - {self.product}'

    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        "products.Product",
        related_name = "reviews",
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey( # if you call it user, I think it can clash with django fields so I tend to use owner
        "jwt_auth.User",
        related_name="reviews",
        on_delete=models.CASCADE,
    )