from django.db import models


class AboutUs(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    logo = models.ImageField(upload_to='shop_logo')
    description = models.TextField()

    def __str__(self):
        return self.name
