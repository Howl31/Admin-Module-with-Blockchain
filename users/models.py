from django.db import models

# Create your models here.


class UserDetail(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class HashTable(models.Model):
    previous_hash = models.CharField(max_length=150, null=True, blank=True)
    user = models.OneToOneField(UserDetail, on_delete=models.CASCADE, null=True, blank=True)
    current_hash = models.CharField(max_length=150, null=True, blank=True)