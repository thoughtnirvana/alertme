from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.cache import cache
from alertme.accounts.models import UserProfile, StockUserRelation
from alertme.stocks.models import Stock
import urllib2
from urllib import quote
import json,re,pdb

def sendAlert():
  users = User.objects.all()
  for user in users:
    userprofile = UserProfile.objects.filter(user=user)
    if userprofile:
      if not userprofile[0].email_alert and not userprofile[0].sms_alert:
        exit(0)
      alert_checks = StockUserRelation.objects.filter(user=user)
      if alert_checks:
        name = user.username
        ph = userprofile[0].ph
        email = user.email
        for alert in alert_checks:
          stock_id = alert.stock_id
          stock_data = cache.get(stock_id)
          if stock_data is None:
            continue
          stock_data = json.loads(stock_data)
          if  not re.search('Rs', stock_data[0]['l_cur']):
            continue
          current_price = int(float(stock_data[0]['l_cur'].replace(",","")[3:]))
          if alert.min_price > 0:
            if current_price <= alert.min_price:
              message = 'Hi ' + name + ". "  + stock_data[0]['name'] + ' has reached the minimum price of ' + stock_data[0]['l_cur']
              print  message
              email = EmailMessage('Stock Alert', message, to=[email])
              email.send()
          if alert.max_price > 0:
            if current_price >= alert.max_price:
              message = 'Hi ' + name + ". "  + stock_data[0]['name'] + ' has reached the maximum price of ' + stock_data[0]['l_cur']
              print  message
              email = EmailMessage('Stock Alert', message, to=[email])
              email.send()

sendAlert()

