#from django.http import HttpResponse, HttpResponseRedirect
#from django.shortcuts import render_to_response
#from django.contrib import auth
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.decorators import login_required
#from alertme.users.models import UserProfile
#from django.core.exceptions import ObjectDoesNotExist
#from django.core.context_processors import csrf
#from django import forms
#import  datetime
#import urllib2
#from urllib import quote
#import json, pdb
#
#google_url = "http://finance.google.com/finance/info?client=ig&q="
#
#def index(request):
#  #now = datetime.datetime.now()
#  #html = "<html><body> It is %s </body></html>" % now
#  #return HttpResponse(html)
#  #data = get_data('507685')
#  #c = {}
#  #c.update(csrf(request))
#  if request.user.is_authenticated():
#    #html = "<html><body> You are logged in as %s </body></html>" % request.user.username
#    #return HttpResponse(html)
#    return HttpResponseRedirect("/loggedin/")
#  else:
#    form = UserCreationForm()
#    return render_to_response('index.html')
#    #html = "<html><body> You are logged in as %s </body></html>" % request.user.username
#    #return HttpResponse(html)
#
#
#def register(request):
#  #c = {}
#  #c.update(csrf(request))
#  if request.method == 'POST':
#    form =UserCreationForm(request.POST)
#    if form.is_valid():
#      new_user = form.save()
#      return HttpResponseRedirect("/loggedin/")
#  else:
#    form = UserCreationForm()
#  return render_to_response('index.html', {'form': form})
#
#def login(request):
#  username = request.POST.get('username', '')
#  password = request.POST.get('password', '')
#  user = auth.authenticate(username=username, password=password)
#  if user is not None and user.is_active:
#    # Correct password, and the user is marked "active"
#    auth.login(request, user)
#    # Redirect to a success page.
#    return HttpResponseRedirect("/loggedin/")
#  else:
#    # Show an error page
#    return HttpResponseRedirect("/invalid/")
#
#def logout(request):
#  auth.logout(request)
#  # Redirect to a success page.
#  return HttpResponseRedirect("/loggedout/")
#
#def get_data(code):
#  values = []
#  stock_url = google_url + quote(code)
#  urlhandle = urllib2.urlopen(stock_url)
#  data = urlhandle.read()
#  if data:
#    data = json.loads(data[3:])
#    data[0]['name'] = 'wipro'
#    data = json.dumps(data)
#    return data
#  #pdb.set_trace()
#  return {}
#
#@login_required
#def get_userprofile(user):
#  try:
#    profile = user.get_profile()
#  except ObjectDoesNotExist:
#    return HttpResponseRedirect("/edit/")
#  return profile
#
#@login_required
#def loggedin(request):
#  html = "<html><body> You are logged in as %s </body></html>" % request.user.username
#  return HttpResponse(html)
#
#@login_required
#def loggedout(request):
#  html = "<html><body> You have been successfully logged out</body></html>"
#  return HttpResponse(html)
#
#@login_required
#def invalid(request):
#  html = "<html><body> Invalid user name or password </body></html>"
#  return HttpResponse(html)
#
