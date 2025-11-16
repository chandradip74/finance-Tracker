from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True, auto_created=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    userrole = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
    )

    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    password = models.TextField()

    def __str__(self):
        return f"{self.username} ({self.userrole})"
