from django.db import models
from user.models import CustomUser
# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key = True , unique=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    stock_quantity = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.name} of {self.from_user.username}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, to_field = "id" , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)



class OrderItem(models.Model):
    product = models.ForeignKey(Product, to_field = "id" , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orders = models.ManyToManyField(OrderItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)


