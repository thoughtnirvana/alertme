# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from alertme.accounts.models import *
from alertme.stocks.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pdb, re, json
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib import messages
from django.core.cache import cache

def signup(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect("/home/")
  if request.method == 'POST':
    form = SignupForm(data=request.POST)
    if form.is_valid():
      new_user=form.save()
      return HttpResponseRedirect("/login/")
  else:
    form = SignupForm()
  return render_to_response('accounts/signup.html', {'form':form}, context_instance=RequestContext(request))

def logout_view(request):
  logout(request)
  return HttpResponseRedirect("/login/")

def login_view(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect("/home/")
  else:
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponseRedirect("/home/")
      else:
        return HttpResponseRedirect("/invalid/")
    else:
      return render_to_response('accounts/login.html',context_instance=RequestContext(request))

@login_required
def user_settings(request):
  user = request.user
  ph='000000000000'
  email_alert = 0 
  sms_alert = 0
  if request.method == 'POST':
    userinfo = UserProfile.objects.filter(user=user)
    if userinfo:
      userinfo = UserProfile.objects.get(user=user)
      if userinfo:
        ph = userinfo.ph
    if request.POST.get('ph'):
      ph = request.POST['ph']
    if request.POST.get('emailalerts'):
      email_alert = 1
    if request.POST.get('smsalerts'):
      sms_alert = 1
    try:
      if (len(ph) < 12) or (not re.match("^[0-9]*$", ph)):
        raise ValidationError("Mobile no should be exactly 12 chars including country code and can only contain digits")
    except ValidationError,  e:
      non_field_errors = e.message_dict[NON_FIELD_ERRORS]
      messages.error(request, non_field_errors)
      return render_to_response('accounts/user-settings.html', context_instance=RequestContext(request))
    if not userinfo:
      u = UserProfile(user=user, ph=ph, email_alert=email_alert, sms_alert=sms_alert)
      u.save()
    else:
      userinfo.ph = ph
      userinfo.email_alert = email_alert
      userinfo.sms_alert = sms_alert
      userinfo.save()
    return HttpResponseRedirect("/home/")
  else:
    userinfo = UserProfile.objects.filter(user=user).values()
    if userinfo:
      return render_to_response('accounts/user-settings.html', userinfo[0], context_instance=RequestContext(request))
    else:
      return render_to_response('accounts/user-settings.html', context_instance=RequestContext(request))

@login_required
def user_alerts(request):
  user = request.user
  max_price = 0
  min_price = 0
  active = True
  userinfo = UserProfile.objects.filter(user=user).values()
  if not userinfo[0]['email_alert'] and not userinfo[0]['sms_alert']:
     messages.error(request, 'You have not enabled alerts yet. Enable at least one of them')
     return render_to_response('accounts/user-settings.html', userinfo[0], context_instance=RequestContext(request))
  if request.method == 'POST':
    #userinfo = UserProfile.objects.filter(user=user)
    #if userinfo:
    #  userinfo = UserProfile.objects.get(user=user)
    #  if userinfo:
    #    ph = userinfo.ph
    #if request.POST.getlist('stockid'):
    stock_id_list = request.POST.getlist('stockid')
    length = len(stock_id_list)
      #existing = StockUserRelation.objects.filter(user=user, stock=stock_id)
    #if request.POST.getlist('upperlimit'):
    max_price_list = request.POST.getlist('upperlimit')
    #if request.POST.getlist('lowerlimit'):
    min_price_list = request.POST.getlist('lowerlimit')
    if length>0:
      for i in range(length):
        try:
          if max_price_list[i]:
            if max_price_list[i] < 0 or (not re.match("^[0-9]*$", max_price_list[i])):
              raise ValidationError("All the prices should be greater than 0 (min<max) and cannnot contain alphabets or special characters")
            else:
              max_price = int(max_price_list[i])
          else:
            max_price = 0
          if min_price_list[i]:
            if min_price_list[i] < 0 or (not re.match("^[0-9]*$", min_price_list[i])):
              raise ValidationError("All the prices should be greater than 0 (min<max) and cannnot contain alphabets or special characters")
            else:
              min_price = int(min_price_list[i])
          else:
            min_price = 0
          if max_price_list[i] and min_price_list[i] and max_price_list[i]<min_price_list[i]:
            raise ValidationError("Max price should be greater than Min price")
        except ValidationError,  e:
          non_field_errors = e.message_dict[NON_FIELD_ERRORS]
          messages.error(request, non_field_errors)
          return render_to_response('accounts/user-alerts.html', context_instance=RequestContext(request))
        stock_id=Stock.objects.get(id=stock_id_list[i])
        existing = StockUserRelation.objects.filter(user=user, stock=stock_id)
        if not existing:
          relation = StockUserRelation(user=user, stock=stock_id, max_price=max_price, min_price=min_price, active=active)
          relation.save()
        else:
          existing = StockUserRelation.objects.get(user=user, stock=stock_id)
          existing.max_price = max_price_list[i]
          existing.min_price = min_price_list[i]
          existing.save()
    return HttpResponseRedirect("/home/")
  else:
    stocks = Stock.objects.all().values()
    user_stock_relation = StockUserRelation.objects.filter(user=user)
    list_for_template = []
    for i in stocks:
      stock_id = i['id']
      stock_data = cache.get(stock_id)
      if stock_data is None:
        continue
      stock_data = json.loads(stock_data)
      if  not re.search('Rs', stock_data[0]['l_cur']):
        continue
      current_price = stock_data[0]['l_cur']
      i['current_price'] = current_price
      if user_stock_relation:
        stock = Stock.objects.filter(id=stock_id)
        user_stock = StockUserRelation.objects.filter(user=user, stock=stock)
        if user_stock:
          i['max_price'] = user_stock[0].max_price
          i['min_price'] = user_stock[0].min_price
          i['alert-set'] = True
      list_for_template.append(i)
    #if userinfo:
    return render_to_response('accounts/user-alerts.html', {'result_list': list_for_template}, context_instance=RequestContext(request))
    #else:
    #  return render_to_response('accounts/user-alerts.html', context_instance=RequestContext(request))
    #return HttpResponseRedirect("/home/")
    #user-stock-relation = StockUserRelation.objects.filter(user=user).values()

@login_required
def home(request):
  #html = "<html><body>Successfully logged in as  %s <a href='/logout/'>Log Out</a> </body></html>" % request.user.username
  return render_to_response('accounts/user-home.html', context_instance=RequestContext(request))
  #return HttpResponse(html)

def invalid(request):
  html = "<html><body>Invalid login credentials</body></html>"
  return HttpResponse(html)
