from django.db import models
from django.contrib.auth.models import User

# Model for car
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.make} {self.model}"

# Extend User model for user details (optional)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# Model for rental record
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

    def __str__(self):
        return f"Rental of {self.car.make} {self.car.model} by {self.user.username}"
