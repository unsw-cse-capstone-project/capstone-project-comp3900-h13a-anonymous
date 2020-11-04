from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Stock(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)

    def publish(self):
        self.save()

    def __str__(self):
        return self.code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=10000)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class WatchListItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock.code

class WatchListAlert(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    watchprice = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    triggered = models.BooleanField(default=False)
    shown = models.BooleanField(default=False)
    dateTriggered = models.CharField(max_length=40)
    action = models.CharField(max_length=4, default='buy') # buy / sell

    def  __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('dateTriggered',)

class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    dateBought = models.CharField(max_length=30)
    orignialUnitBought = models.PositiveIntegerField()
    unitSold = models.PositiveIntegerField()
    
    

class Transaction(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    units = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    
