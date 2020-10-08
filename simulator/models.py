from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
    price = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    