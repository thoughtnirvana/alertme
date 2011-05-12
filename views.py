from django.http import HttpResponse
import  datetime
import urllib2
from urllib import quote
import json
import pdb

google_url = "http://finance.google.com/finance/info?client=ig&q="

def index(request):
  #now = datetime.datetime.now()
  #html = "<html><body> It is %s </body></html>" % now
  #return HttpResponse(html)
  data = get_data('507685')
  return HttpResponse(data)

def get_data(code):
  values = []
  stock_url = google_url + quote(code)
  urlhandle = urllib2.urlopen(stock_url)
  data = urlhandle.read()
  if data:
    data = json.loads(data[3:])
    data[0]['name'] = 'wipro'
    data = json.dumps(data)
    return data
  #pdb.set_trace()
  return {}



