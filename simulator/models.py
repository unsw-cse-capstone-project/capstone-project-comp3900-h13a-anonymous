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
    date = models.CharField(max_length=30)
    watchprice = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    tiggered = models.BooleanField(default=False)

    def __str__(self):
        return self.stock.code

    def plot_watchlist(self):
        now =  datetime.now().timestamp()
        df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={self.code.code}&resolution=1&from={self.date}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

        print(df)

        date = []
        for d in df['t']:
            date.append(datetime.fromtimestamp(d))
        fig = go.Figure(data=[go.Candlestick(x=date,
                    open=df['o'], high=df['h'],
                    low=df['l'], close=df['c'])
                            ])

        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig.write_html("sample_historical_data.html", full_html = False)


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
    
