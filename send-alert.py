from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.cache import cache
from alertme.users.models import User, StockUserRelation
from alertme.stocks.models import Stock
import urllib2
from urllib import quote
import json,re,pdb

stock_dict = {'506134':'Intellivate Cap', '500209':'Infosys', '532696':'Educomp Sol', '533398':'MUTHOOT FIN', '532299':'TV Eighteen',
    '533217':'Hindustan Media', '532706':'Inox Leisure', '532689':'PVR', '533155':'Jubilant Food', '532848':'Delta Corp', '523261':'Venkys'}
google_url = "http://finance.google.com/finance/info?client=ig&q="

def sendAlert():
  alert_checks = StockUserRelation.objects.all()
  if alert_checks is None:
    print 'no alert set'
    exit(0)
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
    if stock_data is None:
      continue
    stock_data = json.loads(stock_data)
    if  not re.search('Rs', stock_data[0]['l_cur']):
      continue
    current_price = int(float(stock_data[0]['l_cur'].replace(",","")[3:]))
    if current_price <= i.min_price:
      message = 'Hi ' + name + " " + ph + ". " + stock_data[0]['name'] + ' has reached the minimum price of ' + stock_data[0]['l_cur']
      print  message
    elif current_price >= i.max_price:
      message = 'Hi ' + name + " " + ph + ". " + stock_data[0]['name'] + ' has reached the maximum price of ' + stock_data[0]['l_cur']
      print  message

sendAlert()

