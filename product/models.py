from django.db import models
import uuid

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    @property
    def slug(self):
        if " & " in self.title:
            slug = "-".join(i.split(" & "))
        else:
            slug = "-".join(i.split(" "))
        return slug

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    productID = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_DEFAULT,
        default=None, blank=True, null=True)
    # merchantId = models.ForeignKey()

    @property
    def slug(self):
        return str(self.id)

    def __str__(self):
        return f"{self.brand.upper()}-{self.name}"
