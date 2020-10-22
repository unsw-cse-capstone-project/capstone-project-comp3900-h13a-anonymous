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

    def __str__(self):
        return self.date


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    dateBuy = models.DateTimeField()
    dateSell = models.DateTimeField()
    unitBuy = models.PositiveIntegerField()
    unitSell = models.PositiveIntegerField()
