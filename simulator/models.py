from django.db import models

# Create your models here.


class Stock(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.code


class User(models.Model):
    email = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    phoneNo = models.IntegerField()
    balance = models.DecimalField(decimal_places=2, max_digits=10)



class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    watchprice = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    tiggered = models.BooleanField(default=False)

    def __str__(self):
        return self.date


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    dateBought = models.CharField(max_length=30)
    orignialUnitBought = models.PositiveIntegerField()
    unitSold = models.PositiveIntegerField()

class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    units = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    action = models.CharField(max_length=30, primary_key=True)
    
