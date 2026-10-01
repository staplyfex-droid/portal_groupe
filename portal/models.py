from django.db import models
from django.contrib.auth.models import User

class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", related_name="user_accounts")
    name = models.CharField(max_length=20)
    secondname = models.CharField(max_length=20)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    def __str__(self):
        return f"{self.name}{self.description}"


