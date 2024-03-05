from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    file = models.FileField(upload_to="img/", storage=FileSystemStorage(location='pay/static/'), blank=True, null=True)
    category = models.CharField(choices=(("C","Clothes"),("E","Electronics"),("O","Other")),default="O", max_length=1)
    description = models.CharField(max_length=1250,null=True)
    stripe_id = models.CharField(max_length=50, blank=False, null=False, default='')
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    pi = models.CharField(max_length=255,default="")
    quantity = models.IntegerField(default=1)