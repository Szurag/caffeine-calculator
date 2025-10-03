from django.contrib.auth.models import User
from django.db import models

from products.models import Product

class Intake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total_caffeine(self):
        return self.quantity * self.product.caffeine_mg
