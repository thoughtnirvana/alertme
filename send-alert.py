from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.cache import cache
from alertme.users.models import User, StockUserRelation
from alertme.stocks.models import Stock
import urllib2
from urllib import quote
import json
import pdb

stock_dict = {'506134':'Intellivate Cap', '500209':'Infosys', '532696':'Educomp Sol', '533398':'MUTHOOT FIN', '532299':'TV Eighteen',
    '533217':'Hindustan Media', '532706':'Inox Leisure', '532689':'PVR', '533155':'Jubilant Food', '532848':'Delta Corp', '523261':'Venkys'}
google_url = "http://finance.google.com/finance/info?client=ig&q="

def sendAlert():
  foo = cache.get('foo')
  print foo
  alert_checks = StockUserRelation.objects.all()
  for i in alert_checks:
    user_id = i.user_id
    stock_id = i.stock_id
    #using get to retrive only one object. The return val will always be one object because filter is primary key.
    #If more than one objects can be returned as result, use filter
    user = User.objects.get(ph=user_id)
    stock = Stock.objects.get(id=stock_id)
    name = user.name
    ph = user.ph
    stock_data = cache.get(stock_id)
    print stock_data
    stock_data = json.loads(stock_data[3:])
    print stock_data
    print ph
    print name
    print stock_id
    print i.max_price
    print i.min_price
#  for key in stock_dict:
#    stock_url = google_url + quote(key)
#    try:
#      urlhandle = urllib2.urlopen(stock_url)
#      data = urlhandle.read()
#    except:
#      continue
#    if data:
#      data = json.loads(data[3:])
#      data[0]['name'] = stock_dict[key]
#      data = json.dumps(data)
#      cache.set(key, data, 900);

sendAlert()

