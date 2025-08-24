from django.db import models
from django.db.utils import OperationalError, ProgrammingError


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class UserAccount(models.Model):   
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)   # ⚠️ production me hash karna hoga
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    side_img = models.CharField(max_length=255, blank=True, null=True, default='img/1-side.webp')
    front_img = models.CharField(max_length=255, blank=True, null=True, default='img/1-front.webp')

    def __str__(self):
        return self.name


def insert_default_products():
    """Default products auto-insert hone ke liye (app ready hone par call karna)"""
    default_products = [
        {"name": "Dark Night Full Rim Square", "price": 1999, "side_img": "img/1-side.webp", "front_img": "img/1-front.webp"},
        {"name": "Crystal Transparent Full Rim Square", "price": 2999, "side_img": "img/2-side.webp", "front_img": "img/2-front.webp"},
        {"name": "Brown Transparent Full Rim Geometric", "price": 3999, "side_img": "img/3-side.webp", "front_img": "img/3-front.webp"},
        {"name": "Gray Transparent Full Rim Square", "price": 2499, "side_img": "img/4-side.webp", "front_img": "img/4-front.webp"},
        {"name": "Sky Blue Full Rim Square", "price": 3499, "side_img": "img/5-side.webp", "front_img": "img/5-front.webp"},
        {"name": "Silver Full Rim Round", "price": 3799, "side_img": "img/6-side.webp", "front_img": "img/6-front.webp"},
    ]

    try:
        for p in default_products:
            Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "price": p["price"],
                    "side_img": p["side_img"],
                    "front_img": p["front_img"]
                }
            )
    except (OperationalError, ProgrammingError):
        # Agar migration se pehle DB table ready nahi hai
        pass


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payment = models.CharField(max_length=50, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name or 'Unknown'}"
