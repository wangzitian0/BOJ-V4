from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms


#class SignupForm(account.forms.SignupForm):
#    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))


class BojSettingsForm(account.forms.SettingsForm):
    nickname = forms.CharField(max_length=32)
    gender = forms.CharField(max_length=6)
    default_lang = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
    	super(BojSettingsForm, self).__init__(*args, **kwargs)
    	self.fields.pop('timezone')
    	self.fields.pop('language')



class BojUserForm(account.forms.SignupForm):
    nickname = forms.CharField(max_length=32)
    gender = forms.CharField(max_length=6)
    default_lang = forms.CharField(max_length=10)
