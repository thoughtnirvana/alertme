from django.db import models
from django.contrib.auth.models import User
from django import forms
from alertme.stocks.models import Stock
from django.core.exceptions import ValidationError
import re

# Create your models here.
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  ph = models.CharField(max_length=12)
  email_alert = models.BooleanField(default=1)
  sms_alert = models.BooleanField(default=0)

  def clean(self):
    if (len(self.ph) < 12) or (not re.match("^[0-9]*$", self.ph)):
        raise ValidationError("Ph no should be exactly 12 chars including country code and can only contain digits")

class StockUserRelation(models.Model):
  user = models.ForeignKey(User)
  stock = models.ForeignKey(Stock)
  max_price = models.IntegerField(default=0)
  min_price = models.IntegerField(default=0)
  alert_sent = models.BooleanField(default=False)
  active = models.BooleanField(default=True)

  def clean(self):
    if self.max_price < 0 or self.min_price < 0 or (not re.match("^[0-9]*$", self.max_price)) or (not re.match("^[0-9]*$", self.min_price)):
      raise ValidationError("All the prices should be greater than 0 (min<max) and cannnot contain alphabets or special characters")
    if self.max_price and self.min_price and self.max_price<self.min_price:
      raise ValidationError("Max price should be greater then Min price")

class SignupForm(forms.Form):
  username = forms.CharField(max_length=30)
  email = forms.EmailField()
  password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))
  password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))

  def clean_username(self):
    try:
      User.objects.get(username=self.cleaned_data['username'])
    except User.DoesNotExist:
      return self.cleaned_data['username']
    raise  forms.ValidationError("This username is already in use. Choose another")

  def clean(self):
    if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
      if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise forms.ValidationError("Passwords do not match")
    return self.cleaned_data

  def save(self):
    new_user = User.objects.create_user(username=self.cleaned_data['username'], 
                                        email=self.cleaned_data['email'], 
                                        password=self.cleaned_data['password1'])
    return new_user





