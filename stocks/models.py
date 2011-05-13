from django.db import models

# Create your models here.
class Stock(models.Model):
  id = models.CharField(max_length=30, primary_key=True)
  name = models.CharField(max_length=80)
  exchange = models.CharField(max_length=80)

  def __unicode__(self):
    return self.name
