from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)

    def __str__(self):
        return self.username
