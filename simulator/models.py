from django.db import models

# Create your models here.


class Stock(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    phoneNo = models.IntegerField()
    balance = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.id


class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.date


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    dateBuy = models.DateTimeField()
    dateSell = models.DateTimeField()
    unitBuy = models.PositiveIntegerField()
    unitSell = models.PositiveIntegerField()
