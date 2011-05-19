# Fetches fresh data for all the stocks listed in the database.
# Runs as a cronjob to keep the cache data live.

from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.cache import cache
from alertme.stocks.models import Stock
import urllib2
from urllib import quote
import json, pdb

google_url = "http://finance.google.com/finance/info?client=ig&q="
def getStockHandle():
  #Retreiving the stocks from DB. It has very few entries at the moment. 
  stocks = Stock.objects.all()
  for i in stocks:
    id = i.id
  cache.set('foo','bar',2100)
  for key in stocks:
    stock_url = google_url + quote(key.id)
    try:
      urlhandle = urllib2.urlopen(stock_url)
      data = urlhandle.read()
    except:
      continue
    if data:
      data = json.loads(data[3:])
      data[0]['name'] = key.name
      data = json.dumps(data)
      cache.set(key.id, data, 900);

getStockHandle()


