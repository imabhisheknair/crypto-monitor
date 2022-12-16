from django.db import models

# Create your models here.
class Users(models.Model):
    chat_id = models.IntegerField() 
    date_added = models.DateTimeField(auto_now_add=True)

class Trader(models.Model):
    username = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

class Positions(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    entryPrice = models.FloatField()
    markPrice = models.FloatField()
    pnl = models.FloatField()
    roe = models.FloatField()
    time = models.DateTimeField()