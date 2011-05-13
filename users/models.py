from django.db import models
from alertme.stocks.models import Stock

# Create your models here.
class User(models.Model):
  ph = models.CharField(primary_key=True, max_length=12)
  name = models.CharField(max_length=80)
  email = models.EmailField()

  def __unicode__(self):
    return self.name

class StockUserRelation(models.Model):
  user = models.ForeignKey(User)
  stock = models.ForeignKey(Stock)
  max_price = models.IntegerField()
  min_price = models.IntegerField()

  def __unicode__(self):
    return self.name
