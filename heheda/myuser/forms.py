from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms


class SignupForm(account.forms.SignupForm):
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))


class SettingsForm(account.forms.SettingsForm):
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))

    def __init__(self, *args, **kwargs):
    	super(SettingsForm, self).__init__(*args, **kwargs)
    	self.fields.pop('timezone')
    	self.fields.pop('language')
